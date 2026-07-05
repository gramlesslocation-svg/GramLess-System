import streamlit as st
import pandas as pd

# 1. PAGE LAYOUT
st.set_page_config(page_title="Gramness Workplace Terminal", page_icon="🌾", layout="centered")

st.title("🌾 Gramness Rice Co.")
st.subheader("Workplace Order Entry & Stock Control Terminal")
st.markdown("---")

# 2. THE STORAGE STOCK ROOM (INVENTORY DATABASE)
# This represents what you have left in the warehouse right now
if "inventory" not in st.session_state:
    st.session_state.inventory = {
        "Rice Team": {"800g": 100, "2.4kg": 50},
        "Rice Gold": {"800g": 100, "2.4kg": 50},
        "Rice White": {"800g": 200, "2.4kg": 100},
        "Rice Creamy": {"800g": 15, "2.4kg": 30}  # Low stock test for Creamy
    }

# This stores the active shipping manifest list
if "order_book" not in st.session_state:
    st.session_state.order_book = []

# ==========================================
# SECTION A: LIVE WAREHOUSE STOCK VIEW
# ==========================================
st.markdown("### 🏬 Current Warehouse Stocks")
# Convert storage records to a simple clean table view
stock_data = []
for rice, sizes in st.session_state.inventory.items():
    for size, qty in sizes.items():
        stock_data.append({"Rice Type": rice, "Pack Size": size, "Boxes Left in Stock": qty})
st.dataframe(pd.DataFrame(stock_data), hide_index=True, use_container_width=True)

st.markdown("---")

# ==========================================
# SECTION B: INTERACTIVE ORDER DESK (WORKER INPUT)
# ==========================================
st.markdown("### 📥 Place New Customer Order")

# Input boxes for the worker
client_name = st.text_input("Customer Name:", placeholder="e.g. John")
location = st.text_input("Delivery City/Location:", placeholder="e.g. Beirut")

# Select boxes for the items
selected_rice = st.selectbox("Select Rice Type:", ["Rice Team", "Rice Gold", "Rice White", "Rice Creamy"])
selected_size = st.selectbox("Select Pack Size:", ["800g", "2.4kg"])
order_qty = st.number_input("How many packs do they want?", min_value=1, value=10, step=1)

# Process order button logic
if st.button("Verify Stocks & Submit Order", type="primary"):
    if client_name == "" or location == "":
        st.error("❌ Please enter a Customer Name and Location first!")
    else:
        # Check if the warehouse has enough items left
        available_stock = st.session_state.inventory[selected_rice][selected_size]
        
        if available_stock >= order_qty:
            # STEP 1: Deduct from stock room immediately
            st.session_state.inventory[selected_rice][selected_size] -= order_qty
            
            # STEP 2: Save order transaction data to the book log
            new_invoice = {
                "id": f"GRM-{len(st.session_state.order_book) + 101}",
                "client": client_name,
                "loc": location,
                "item": f"{selected_rice} ({selected_size})",
                "qty": order_qty,
                "status": "Ready for Packing"
            }
            st.session_state.order_book.insert(0, new_invoice)
            st.success(f"✅ Success! Order logged for {client_name}. Stock deducted.")
            st.rerun()
        else:
            # Deny entry if there isn't enough inventory items left
            st.error(f"🚨 ORDER DENIED! Not enough stock. You want {order_qty} packs, but warehouse only has {available_stock} packs left of {selected_rice} ({selected_size}).")

st.markdown("---")

# ==========================================
# SECTION C: OUTBOUND SHIPPING CHECKLIST
# ==========================================
st.markdown("### 🚚 Outbound Dispatch Shipping Manifest")

if len(st.session_state.order_book) == 0:
    st.info("No active pending orders to ship yet.")
else:
    for idx, order in enumerate(st.session_state.order_book):
        with st.expander(f"📦 Receipt {order['id']} - {order['client']} ({order['loc']})"):
            st.markdown(f"**Item Needed:** {order['item']}")
            st.markdown(f"**Quantity to Pack:** {order['qty']} pieces")
            st.markdown(f"**Current Status:** `{order['status']}`")
            
            # Action button for warehouse loader to clear it out
            if order['status'] == "Ready for Packing":
                if st.button(f"Mark Order {order['id']} as Dispatched/Shipped", key=f"ship_{order['id']}"):
                    st.session_state.order_book[idx]['status'] = "Shipped Out"
                    st.rerun()
