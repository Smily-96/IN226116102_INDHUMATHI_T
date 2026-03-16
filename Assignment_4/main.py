from fastapi import FastAPI, HTTPException
from fastapi import Query

app = FastAPI()

# Initial Products
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
]

# Home
@app.get("/")
def home():
    return {"message": "Welcome to E-commerce API"}

# Get all products
@app.get("/products")
def get_products():
    return {"products": products, "total": len(products)}

# Add product
@app.post("/products")
def add_product(name: str, price: int, category: str, in_stock: bool):

    for p in products:
        if p["name"].lower() == name.lower():
            raise HTTPException(status_code=400, detail="Product already exists")

    new_product = {
        "id": len(products) + 1,
        "name": name,
        "price": price,
        "category": category,
        "in_stock": in_stock
    }

    products.append(new_product)

    return {"message": "Product added", "product": new_product}

# Update product
@app.put("/products/update/{product_id}")
def update_product(product_id: int, price: int = None, in_stock: bool = None):

    for p in products:
        if p["id"] == product_id:

            if price is not None:
                p["price"] = price

            if in_stock is not None:
                p["in_stock"] = in_stock

            return {"message": "Product updated", "product": p}

    raise HTTPException(status_code=404, detail="Product not found")

# Delete product
@app.delete("/products/delete/{product_id}")
def delete_product(product_id: int):

    for p in products:
        if p["id"] == product_id:
            products.remove(p)
            return {"message": f"Product '{p['name']}' deleted"}

    raise HTTPException(status_code=404, detail="Product not found")

# Inventory audit
@app.get("/products/audit")
def audit():

    total_products = len(products)

    in_stock_products = [p for p in products if p["in_stock"]]

    out_of_stock_names = [p["name"] for p in products if not p["in_stock"]]

    total_stock_value = sum(p["price"] * 10 for p in in_stock_products)

    most_expensive = max(products, key=lambda x: x["price"])

    return {
        "total_products": total_products,
        "in_stock_count": len(in_stock_products),
        "out_of_stock_names": out_of_stock_names,
        "total_stock_value": total_stock_value,
        "most_expensive": {
            "name": most_expensive["name"],
            "price": most_expensive["price"]
        }
    }


# BONUS — Apply Category Discount
@app.put("/products/discount")
def bulk_discount(
    category: str = Query(...),
    discount_percent: int = Query(..., ge=1, le=99)
):

    updated = []

    for p in products:
        if p["category"].lower() == category.lower():
            p["price"] = int(p["price"] * (1 - discount_percent / 100))
            updated.append({
                "name": p["name"],
                "new_price": p["price"]
            })

    if not updated:
        return {"message": f"No products found in category: {category}"}

    return {
        "message": f"{discount_percent}% discount applied to {category}",
        "updated_count": len(updated),
        "updated_products": updated
    }

# Get product by id (THIS MUST BE LAST)
@app.get("/products/{product_id}")
def get_product(product_id: int):
    for p in products:
        if p["id"] == product_id:
            return {"product": p}

    raise HTTPException(status_code=404, detail="Product not found")

# ---------------- CART SYSTEM ----------------

cart = []
orders = []
order_counter = 1


# ADD TO CART
@app.post("/cart/add")
def add_to_cart(product_id: int, quantity: int = 1):

    for product in products:

        if product["id"] == product_id:

            if not product["in_stock"]:
                raise HTTPException(
                    status_code=400,
                    detail=f"{product['name']} is out of stock"
                )

            # Check if product already in cart
            for item in cart:
                if item["product_id"] == product_id:
                    item["quantity"] += quantity
                    item["subtotal"] = item["quantity"] * item["unit_price"]

                    return {
                        "message": "Cart updated",
                        "cart_item": item
                    }

            cart_item = {
                "product_id": product_id,
                "product_name": product["name"],
                "quantity": quantity,
                "unit_price": product["price"],
                "subtotal": product["price"] * quantity
            }

            cart.append(cart_item)

            return {
                "message": "Added to cart",
                "cart_item": cart_item
            }

    raise HTTPException(status_code=404, detail="Product not found")


# VIEW CART
@app.get("/cart")
def view_cart():

    if not cart:
        return {"message": "Cart is empty"}

    grand_total = sum(item["subtotal"] for item in cart)

    return {
        "items": cart,
        "item_count": len(cart),
        "grand_total": grand_total
    }


# REMOVE FROM CART
@app.delete("/cart/{product_id}")
def remove_from_cart(product_id: int):

    for item in cart:
        if item["product_id"] == product_id:
            cart.remove(item)
            return {"message": f"{item['product_name']} removed from cart"}

    raise HTTPException(status_code=404, detail="Item not in cart")


# CHECKOUT
@app.post("/cart/checkout")
def checkout(customer_name: str, delivery_address: str):

    global order_counter

    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")

    placed_orders = []

    for item in cart:

        order = {
            "order_id": order_counter,
            "customer_name": customer_name,
            "product": item["product_name"],
            "quantity": item["quantity"],
            "total_price": item["subtotal"],
            "delivery_address": delivery_address
        }

        orders.append(order)
        placed_orders.append(order)

        order_counter += 1

    cart.clear()

    return {
        "message": "Checkout successful",
        "orders_placed": placed_orders
    }


# VIEW ORDERS
@app.get("/orders")
def view_orders():

    return {
        "orders": orders,
        "total_orders": len(orders)
    }