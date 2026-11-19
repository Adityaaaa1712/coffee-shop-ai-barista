import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

def init_cart() -> Dict:
    return {
        "items": [],
        "total": 0.0
    }

def add_to_cart(cart: Dict, item: Dict, quantity: int = 1) -> Dict:
    for cart_item in cart["items"]:
        if cart_item["id"] == item["id"]:
            cart_item["quantity"] += quantity
            cart["total"] = calculate_total(cart)
            return cart
    
    cart["items"].append({
        "id": item["id"],
        "name": item["name"],
        "price": item["price"],
        "quantity": quantity
    })
    cart["total"] = calculate_total(cart)
    return cart

def remove_from_cart(cart: Dict, item_id: int) -> Dict:
    cart["items"] = [item for item in cart["items"] if item["id"] != item_id]
    cart["total"] = calculate_total(cart)
    return cart

def update_quantity(cart: Dict, item_id: int, quantity: int) -> Dict:
    if quantity <= 0:
        return remove_from_cart(cart, item_id)
    
    for cart_item in cart["items"]:
        if cart_item["id"] == item_id:
            cart_item["quantity"] = quantity
            break
    
    cart["total"] = calculate_total(cart)
    return cart

def calculate_total(cart: Dict) -> float:
    return round(sum(item["price"] * item["quantity"] for item in cart["items"]), 2)

def clear_cart(cart: Dict) -> Dict:
    return init_cart()

def save_order_to_session(cart: Dict, orders: list, customer_name: str = "Guest") -> Dict:
    """Save order to session state list (session-only, not persisted to disk)"""
    order_id = len(orders) + 1
    order = {
        "order_id": order_id,
        "timestamp": datetime.now().isoformat(),
        "customer_name": customer_name,
        "items": cart["items"].copy(),  # Copy to avoid reference issues
        "total": cart["total"]
    }
    orders.append(order)
    return order

def save_order(cart: Dict, customer_name: str = "Guest") -> Dict:
    orders_path = Path(__file__).parent / "data" / "orders.json"
    
    if orders_path.exists():
        with open(orders_path, "r", encoding="utf-8") as f:
            orders = json.load(f)
    else:
        orders = []
    
    order_id = len(orders) + 1
    order = {
        "order_id": order_id,
        "timestamp": datetime.now().isoformat(),
        "customer_name": customer_name,
        "items": cart["items"],
        "total": cart["total"]
    }
    
    orders.append(order)
    
    with open(orders_path, "w", encoding="utf-8") as f:
        json.dump(orders, f, indent=2)
    
    return order
