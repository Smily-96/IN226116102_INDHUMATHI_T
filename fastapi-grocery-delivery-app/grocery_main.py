from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# ---------------- ITEMS ----------------

items = [
    {"id": 1, "name": "Tomatoes", "price": 40, "unit": "kg", "category": "Vegetable", "in_stock": True},
    {"id": 2, "name": "Milk", "price": 60, "unit": "litre", "category": "Dairy", "in_stock": True},
    {"id": 3, "name": "Rice", "price": 1200, "unit": "kg", "category": "Grain", "in_stock": True},
    {"id": 4, "name": "Eggs", "price": 6, "unit": "piece", "category": "Dairy", "in_stock": True},
    {"id": 5, "name": "Apple", "price": 120, "unit": "kg", "category": "Fruit", "in_stock": True},
    {"id": 6, "name": "Wheat Flour", "price": 55, "unit": "kg", "category": "Grain", "in_stock": False},
]

# ---------------- HOME ----------------

@app.get("/")
def home():
    return {"message": "Welcome to FreshMart Grocery"}

# ---------------- GET ITEMS ----------------

@app.get("/items")
def get_items():
    in_stock_count = len([i for i in items if i["in_stock"]])
    return {"items": items, "total": len(items), "in_stock_count": in_stock_count}

# ---------------- SUMMARY ----------------

@app.get("/items/summary")
def summary():
    in_stock = len([i for i in items if i["in_stock"]])
    out_stock = len(items) - in_stock

    category_count = {}
    for i in items:
        category_count[i["category"]] = category_count.get(i["category"], 0) + 1

    return {
        "total_items": len(items),
        "in_stock": in_stock,
        "out_of_stock": out_stock,
        "category_breakdown": category_count
    }



# ---------------- MODELS ----------------

class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    item_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=50)
    delivery_address: str = Field(..., min_length=10)
    delivery_slot: str = "Morning"
    bulk_order: bool = False

class NewItem(BaseModel):
    name: str = Field(..., min_length=2)
    price: int = Field(..., gt=0)
    unit: str = Field(..., min_length=2)
    category: str = Field(..., min_length=2)
    in_stock: bool = True

# ---------------- HELPERS ----------------

def find_item(item_id):
    for i in items:
        if i["id"] == item_id:
            return i
    return None

def calculate_total(price, quantity, slot, bulk):
    original = price * quantity

    discount = 0
    if bulk and quantity >= 10:
        discount = original * 0.08

    after_discount = original - discount

    delivery = 0
    if slot == "Morning":
        delivery = 40
    elif slot == "Evening":
        delivery = 60

    total = after_discount + delivery

    return {
        "original": original,
        "discount": discount,
        "delivery": delivery,
        "final": total
    }

# ---------------- CREATE ORDER ----------------

orders = []
order_counter = 1

@app.post("/orders")
def create_order(order: OrderRequest):
    global order_counter

    item = find_item(order.item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if not item["in_stock"]:
        raise HTTPException(status_code=400, detail="Item out of stock")

    cost = calculate_total(item["price"], order.quantity, order.delivery_slot, order.bulk_order)

    new_order = {
        "order_id": order_counter,
        "customer_name": order.customer_name,
        "item": item["name"],
        "quantity": order.quantity,
        "unit": item["unit"],
        "delivery_slot": order.delivery_slot,
        "cost": cost,
        "status": "confirmed"
    }

    orders.append(new_order)
    order_counter += 1

    return new_order

# ---------------- FILTER ----------------

@app.get("/items/filter")
def filter_items(
    category: Optional[str] = None,
    max_price: Optional[int] = None,
    unit: Optional[str] = None,
    in_stock: Optional[bool] = None
):
    result = items

    if category is not None:
        result = [i for i in result if i["category"].lower() == category.lower()]

    if max_price is not None:
        result = [i for i in result if i["price"] <= max_price]

    if unit is not None:
        result = [i for i in result if i["unit"].lower() == unit.lower()]

    if in_stock is not None:
        result = [i for i in result if i["in_stock"] == in_stock]

    return {"items": result, "total": len(result)}

# ---------------- ADD ITEM ----------------

@app.post("/items", status_code=201)
def add_item(item: NewItem):
    for i in items:
        if i["name"].lower() == item.name.lower():
            raise HTTPException(status_code=400, detail="Item already exists")

    new = item.dict()
    new["id"] = len(items) + 1

    items.append(new)
    return new

# ---------------- UPDATE ITEM ----------------

@app.put("/items/{item_id}")
def update_item(item_id: int, price: Optional[int] = None, in_stock: Optional[bool] = None):
    item = find_item(item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if price is not None:
        item["price"] = price

    if in_stock is not None:
        item["in_stock"] = in_stock

    return item

# ---------------- DELETE ITEM ----------------

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for o in orders:
        if o["item"] == find_item(item_id)["name"]:
            raise HTTPException(status_code=400, detail="Item has active orders")

    for i in items:
        if i["id"] == item_id:
            items.remove(i)
            return {"message": "Item deleted"}

    raise HTTPException(status_code=404, detail="Item not found")

# ---------------- CART ----------------

cart = []

@app.post("/cart/add")
def add_to_cart(item_id: int, quantity: int = 1):
    item = find_item(item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if not item["in_stock"]:
        raise HTTPException(status_code=400, detail="Out of stock")

    for c in cart:
        if c["item_id"] == item_id:
            c["quantity"] += quantity
            c["subtotal"] = c["quantity"] * c["price"]
            return c

    new = {
        "item_id": item_id,
        "name": item["name"],
        "quantity": quantity,
        "price": item["price"],
        "subtotal": item["price"] * quantity
    }

    cart.append(new)
    return new

@app.get("/cart")
def view_cart():
    total = sum(c["subtotal"] for c in cart)
    return {"items": cart, "total": total}

@app.delete("/cart/{item_id}")
def remove_cart(item_id: int):
    for c in cart:
        if c["item_id"] == item_id:
            cart.remove(c)
            return {"message": "Removed"}
    raise HTTPException(status_code=404, detail="Not in cart")

@app.post("/cart/checkout", status_code=201)
def checkout(customer_name: str, delivery_address: str, delivery_slot: str = "Morning"):
    global order_counter

    if not cart:
        raise HTTPException(status_code=400, detail="Cart empty")

    placed = []
    total = 0

    for c in cart:
        order = {
            "order_id": order_counter,
            "customer_name": customer_name,
            "item": c["name"],
            "quantity": c["quantity"],
            "delivery_slot": delivery_slot,
            "total_price": c["subtotal"]
        }

        total += c["subtotal"]
        orders.append(order)
        placed.append(order)
        order_counter += 1

    cart.clear()

    return {"orders": placed, "grand_total": total}

# ---------------- SEARCH ----------------

@app.get("/items/search")
def search(keyword: str = Query(...)):
    result = [i for i in items if keyword.lower() in i["name"].lower() or keyword.lower() in i["category"].lower()]
    return {"total_found": len(result), "items": result}

# ---------------- SORT ----------------

@app.get("/items/sort")
def sort(sort_by: str = "price", order: str = "asc"):
    if sort_by not in ["price", "name", "category"]:
        raise HTTPException(status_code=400)

    result = sorted(items, key=lambda x: x[sort_by], reverse=(order == "desc"))
    return {"items": result}

# ---------------- PAGINATION ----------------

@app.get("/items/page")
def page(page: int = 1, limit: int = 4):
    start = (page - 1) * limit
    return {
        "page": page,
        "total_pages": -(-len(items)//limit),
        "items": items[start:start+limit]
    }

# ---------------- ORDERS ----------------

@app.get("/orders")
def get_orders():
    return {"orders": orders, "total": len(orders)}

@app.get("/orders/search")
def search_orders(customer_name: str):
    result = [o for o in orders if customer_name.lower() in o["customer_name"].lower()]
    return {"orders": result}

@app.get("/orders/page")
def page_orders(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    return {
        "page": page,
        "orders": orders[start:start+limit]
    }

# ---------------- BROWSE ----------------

@app.get("/items/browse")
def browse(
    keyword: Optional[str] = None,
    category: Optional[str] = None,
    in_stock: Optional[bool] = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):
    result = items

    if keyword:
        result = [i for i in result if keyword.lower() in i["name"].lower()]

    if category:
        result = [i for i in result if i["category"].lower() == category.lower()]

    if in_stock is not None:
        result = [i for i in result if i["in_stock"] == in_stock]

    result = sorted(result, key=lambda x: x[sort_by], reverse=(order == "desc"))

    start = (page - 1) * limit

    return {
        "total": len(result),
        "items": result[start:start+limit]
    }

# ---------------- GET ITEM BY ID ----------------

@app.get("/items/{item_id}")
def get_item(item_id: int):
    for i in items:
        if i["id"] == item_id:
            return {"item": i}
    raise HTTPException(status_code=404, detail="Item not found")