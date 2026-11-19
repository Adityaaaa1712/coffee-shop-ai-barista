import streamlit as st
import re
from agent import BaristaAgent
from menu_search import load_menu
from cart_manager import init_cart, add_to_cart, remove_from_cart, update_quantity, clear_cart, save_order_to_session
import config

st.set_page_config(
    page_title="☕ Coffee Shop",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    div[data-testid="element-container"]:has(.header-container),
    div.element-container:has(.header-container) {
        position: sticky;
        top: 2.875rem;
        z-index: 999;
        background-color: transparent;
        padding-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-container" style="text-align: center; padding: 20px; background: linear-gradient(135deg, #8B5E3C, #6F4E37); color: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
    <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700; color: white;">☕ Coffee Shop</h1>
    <p style="margin: 5px 0 0 0; font-size: 1.1rem; opacity: 0.9; color: white;">Your friendly AI Barista is ready to help you find the perfect drink or pastry!</p>
</div>
""", unsafe_allow_html=True)

if "menu" not in st.session_state:
    st.session_state.menu = load_menu()

if "cart" not in st.session_state:
    st.session_state.cart = init_cart()

if "orders" not in st.session_state:
    st.session_state.orders = []

if "agent" not in st.session_state:
    try:
        api_key = config.get_openai_key()
        st.session_state.agent = BaristaAgent(api_key, st.session_state.menu)
    except Exception as e:
        st.error(f"⚠️ {str(e)}")
        st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to ☕ Coffee Shop! What can I get started for you today?"}
    ]

with st.sidebar:
    st.markdown("## 📋 Menu")
    
    categories = {}
    for item in st.session_state.menu:
        cat = item.get("category", "other")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)
    
    for category, items in categories.items():
        st.markdown(f"### {category.title()}")
        for item in items:
            with st.container(border=True):
                st.markdown(f"**{item['name']}**  •  **${item['price']:.2f}**")
                st.caption(item['description'])
                
                tags = " ".join([f"`{t}`" for t in item.get("tags", [])])
                if tags:
                    st.markdown(tags)
                
                allergens = ", ".join(item.get("allergens", []))
                if allergens:
                    st.markdown(f"⚠️ *Allergens: {allergens}*")
                
                if st.button("Add to Cart", key=f"menu_{item['id']}"):
                    st.session_state.cart = add_to_cart(st.session_state.cart, item)
                    st.rerun()
    
    st.markdown("---")
    st.markdown("## 🛒 Cart")
    
    if st.session_state.cart["items"]:
        for item in st.session_state.cart["items"]:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"**{item['name']}**")
                st.caption(f"${item['price']:.2f} × {item['quantity']}")
            with col2:
                if st.button("−", key=f"dec_{item['id']}"):
                    st.session_state.cart = update_quantity(st.session_state.cart, item['id'], item['quantity'] - 1)
                    st.rerun()
            with col3:
                if st.button("+", key=f"inc_{item['id']}"):
                    st.session_state.cart = update_quantity(st.session_state.cart, item['id'], item['quantity'] + 1)
                    st.rerun()
        
        st.markdown(f"### Total: ${st.session_state.cart['total']:.2f}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear Cart"):
                st.session_state.cart = clear_cart(st.session_state.cart)
                st.rerun()
        with col2:
            if st.button("Checkout", type="primary"):
                order = save_order_to_session(st.session_state.cart, st.session_state.orders)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"✅ Order #{order['order_id']} confirmed! Total: ${order['total']:.2f}. Thank you for your order!"
                })
                st.session_state.cart = clear_cart(st.session_state.cart)
                st.rerun()
    else:
        st.info("Your cart is empty")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask for recommendations or add items to cart"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        response = st.session_state.agent.get_response(
            prompt,
            [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]]
        )
        
        # Cart action detection
        cart_pattern = r'\[CART_ADD:(\d+)\]'
        cart_matches = re.findall(cart_pattern, response)
        
        if cart_matches:
            for item_id_str in cart_matches:
                item_id = int(item_id_str)
                menu_item = next((item for item in st.session_state.menu if item['id'] == item_id), None)
                
                if menu_item:
                    st.session_state.cart = add_to_cart(st.session_state.cart, menu_item)
            
            # Remove tags from display
            response = re.sub(cart_pattern, '', response).strip()
        
        # Checkout action detection
        checkout_pattern = r'\[CHECKOUT\]'
        checkout_match = re.search(checkout_pattern, response)
        
        if checkout_match:
            if st.session_state.cart["items"]:
                # Trigger checkout
                order = save_order_to_session(st.session_state.cart, st.session_state.orders)
                # Add system confirmation to messages (AI message already has friendly text)
                response = re.sub(checkout_pattern, '', response).strip()
                response += f"\n\n✅ **Order #{order['order_id']} confirmed!** Total: ${order['total']:.2f}"
                st.session_state.cart = clear_cart(st.session_state.cart)
            else:
                # Cart empty - remove tag, let AI message show
                response = re.sub(checkout_pattern, '', response).strip()
        
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        if cart_matches or checkout_match:
            st.rerun()
