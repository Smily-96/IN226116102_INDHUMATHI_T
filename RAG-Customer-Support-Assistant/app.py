from typing import TypedDict

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langgraph.graph import StateGraph, END


# -------------------------------
# Step 1: Load and prepare PDF
# -------------------------------
loader = PyPDFLoader("data/knowledge_base.pdf")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
chunks = text_splitter.split_documents(documents)

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    cache_folder="models"
)

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="chroma_db"
)

print("RAG system with LangGraph + HITL is ready!")


# -------------------------------
# Step 2: Define graph state
# -------------------------------
class GraphState(TypedDict):
    query: str
    retrieved_chunks: str
    answer: str
    needs_human: bool


# -------------------------------
# Step 3: Processing node
# -------------------------------
def process_query(state: GraphState) -> GraphState:
    query = state["query"]
    query_lower = query.lower().strip()

    # Retrieve relevant chunks
    results = vector_store.similarity_search(query, k=2)
    retrieved_text = "\n\n".join([doc.page_content for doc in results])

    # -------------------------------
    # Condition block
    # -------------------------------
    escalation_keywords = ["complaint", "legal", "angry", "manager", "escalate", "lawsuit"]

    if any(word in query_lower for word in escalation_keywords):
        answer = "This issue is being escalated to a human support agent."
        needs_human = True

    elif any(word in query_lower for word in ["refund", "return", "not interested", "dont want", "don't want"]):
        answer = (
            "According to the knowledge base, if you are not interested in the product, "
            "you may request a refund or return. Refunds are allowed when the product is "
            "damaged, wrong, or defective. The request must be made within 7 days of delivery, "
            "and the product must be unused and in its original packaging."
        )
        needs_human = False

    elif any(word in query_lower for word in ["cancel", "cancellation"]):
        answer = (
            "According to the knowledge base, orders can be cancelled before shipment. "
            "Once the order is shipped, cancellation is not allowed."
        )
        needs_human = False

    elif any(word in query_lower for word in ["shipping", "delivery", "ship", "delivered"]):
        answer = (
            "According to the knowledge base, standard shipping takes 3–5 business days, "
            "express shipping takes 1–2 business days, and international shipping may take 7–14 business days."
        )
        needs_human = False

    elif any(word in query_lower for word in ["payment", "paid", "money deducted", "transaction"]):
        answer = (
            "According to the knowledge base, accepted payment methods include credit/debit card, "
            "UPI, net banking, and wallets. If payment fails or money is deducted without order confirmation, "
            "the amount will be refunded within 3–5 business days."
        )
        needs_human = False

    elif any(word in query_lower for word in ["password", "account", "login", "sign in"]):
        answer = (
            "According to the knowledge base, customers can reset their password using the "
            "'Forgot Password' option and follow the instructions sent to their registered email."
        )
        needs_human = False

    else:
        answer = "I found relevant information in the document, but this query requires human review."
        needs_human = True

    return {
        "query": query,
        "retrieved_chunks": retrieved_text,
        "answer": answer,
        "needs_human": needs_human
    }


# -------------------------------
# Step 4: Output node
# -------------------------------
def output_result(state: GraphState) -> GraphState:
    print("\nUser Question:")
    print(state["query"])

    print("\nTop Retrieved Chunks:\n")
    print(state["retrieved_chunks"])

    print("\nFinal Answer:\n")
    print(state["answer"])

    if state["needs_human"]:
        print("\nStatus: Escalated to Human Support")
    else:
        print("\nStatus: Answered by RAG Assistant")

    return state


# -------------------------------
# Step 5: Build LangGraph
# -------------------------------
builder = StateGraph(GraphState)

builder.add_node("process", process_query)
builder.add_node("output", output_result)

builder.set_entry_point("process")
builder.add_edge("process", "output")
builder.add_edge("output", END)

graph = builder.compile()


# -------------------------------
# Step 6: Run the graph
# -------------------------------
user_query = input("\nEnter your customer support question: ")

graph.invoke({
    "query": user_query,
    "retrieved_chunks": "",
    "answer": "",
    "needs_human": False
})