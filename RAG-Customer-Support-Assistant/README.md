# 📌 RAG-Based Customer Support Assistant (LangGraph + HITL)

## 🚀 Project Overview

This project implements a **Retrieval-Augmented Generation (RAG)** based Customer Support Assistant using:

- 📄 PDF Knowledge Base
- 🔍 Semantic Search (Embeddings + ChromaDB)
- 🔁 LangGraph Workflow
- 👨‍💼 Human-in-the-Loop (HITL) Escalation

The system retrieves relevant information from a document and generates contextual responses. It also intelligently escalates sensitive queries to human support.

---

## 🎯 Key Features

- ✅ PDF-based knowledge retrieval
- ✅ Chunking using Recursive Text Splitter
- ✅ Embeddings using HuggingFace
- ✅ Vector storage using ChromaDB
- ✅ LangGraph workflow orchestration
- ✅ Conditional routing (Intent-based)
- ✅ Human-in-the-Loop (HITL) escalation

---

## 🧠 How It Works

1. Load PDF knowledge base  
2. Split into chunks  
3. Convert chunks into embeddings  
4. Store in ChromaDB  
5. User asks a query  
6. Retrieve relevant chunks  
7. Generate response  
8. Apply conditional logic:
   - Normal queries → Answer  
   - Complaint/legal queries → Escalate  

---

## 🔁 LangGraph Workflow
User Input → Processing Node → Output Node → END

- **Processing Node**:
  - Retrieves relevant chunks
  - Detects intent
  - Decides response or escalation

- **Output Node**:
  - Displays retrieved context
  - Shows final answer
  - Indicates escalation status

---

## 👨‍💼 Human-in-the-Loop (HITL)

The system escalates queries if they contain:
- Complaint
- Legal issue
- Angry intent
- Manager request
- Unknown/unclear queries

Example:
Input: I want to file a legal complaint
Output: Escalated to Human Support


---

## 🧪 Sample Queries

| Query | Output |
|------|-------|
| What is the refund policy? | Returns refund details |
| How can I cancel my order? | Returns cancellation info |
| I am not interested in the product | Returns refund/return info |
| I want to file a legal complaint | Escalated to human |

---

## 🛠️ Tech Stack

- Python
- LangChain
- LangGraph
- HuggingFace Embeddings
- ChromaDB
- PyPDF

---

## 📂 Project Structure
rag_project/
├── app.py
├── requirements.txt
├── README.md
├── data/
│ └── knowledge_base.pdf
├── chroma_db/
├── models/


---

## ⚙️ Installation

```bash
pip install -r requirements.txt

▶️ Run the Project
python app.py

Output Example
User Question: What is the refund policy?

Final Answer:
Customers can request a refund within 7 days...

Status: Answered by RAG Assistant

⚠️ Notes
First run may take time due to model download
Internet required only for initial embedding download
Warning about HF_TOKEN can be ignored
🔮 Future Enhancements
Multi-document support
LLM-based answer generation (GPT/Gemini)
Web UI using Streamlit
Memory-based conversation
Feedback loop integration
📌 Conclusion

This project demonstrates the implementation of a scalable AI-powered customer support system using RAG and LangGraph. It effectively combines retrieval-based responses with workflow orchestration and human escalation, making it suitable for real-world applications.

Acknowledgment

Developed as part of the RAG Internship Project at Innomatics Research Labs.