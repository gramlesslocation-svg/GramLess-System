import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime

# ==============================================================================
# 1. APPLICATION & WINDOW CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Gramness ERP System", 
    page_icon="🌾", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Style styling injection for clean metrics look
st.markdown("""
<style>
    .metric-box {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2e7d32;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

st.title("🌾 Gramness Rice Co. - Enterprise Resource System")
st.markdown("### Operational Dashboard, Live Stock Control & Logistic Tracking Matrix")
st.markdown("---")

# ==============================================================================
# 2. SEED DATABASE INITIALIZATION (PERSISTENT DATA MANAGEMENT)
# ==============================================================================
# Initialize core stock ledger records if database is cold
if "inventory" not in st.session_state:
    st.session_state.inventory = {
        "Rice Team": {"800g": 1450, "2.4kg": 620},
        "Rice Gold": {"800g": 980, "2.4kg": 410},
        "Rice White": {"800g": 3200, "2.4kg": 1150},
        "Rice Creamy": {"800g": 750, "2.4kg": 280}
    }

# Initialize transaction log ledger if database is cold
if "orders" not in st.session_state:
    st.session_state.orders = [
        {"id": "GRM-801", "client": "Al-Maha Supermarket", "type": "Rice Gold", "size": "2.4kg", "qty": 40, "revenue": 600, "status": "Delivered", "lat": 33.8938, "lon": 35.5018, "date": "2026-07-05 09:15"},
        {"id": "GRM-802", "client": "Beirut Distribution Hub", "type": "Rice White", "size": "800g", "qty": 150, "revenue": 900, "status": "In Transit", "lat": 33.8869, "lon": 35.5131, "date": "2026-07-05 11:30"},
        {"id": "GRM-803", "client": "Elite Catering Services", "type": "Rice Creamy", "size": "2.4kg", "qty": 15, "revenue": 300, "status": "Processing", "lat": 33.8720, "lon": 35.4850, "date": "2026-07-05 13:02"},
        {"id": "GRM-804", "client": "Global Grain Traders", "type": "Rice Team", "size": "800g", "qty": 300, "revenue": 1500, "status": "Shipped", "lat": 33.9001, "lon": 35.4740, "date": "2026-07-05 14:45"}
    ]

# Price reference book matrix variables
PRICE_BOOK = {
    "800g": 5.00,
    "2.4kg": 12.50
}

# ==============================================================================
# 3. INTERACTIVE SIMULATION MANAGEMENT ENGINE (SIDE PANEL CONTROLS)
# ==============================================================================
st.sidebar.header("🕹️ Simulation Engine Panel")
st.sidebar.markdown("Use these features to instantly mock business events live in front of stakeholders.")

# Operational Metric Simulator Trigger Button
if st.sidebar.button("Simulate Incoming Customer Order", use_container_width=True):
    selected_rice = random.choice(["Rice Team", "Rice Gold", "Rice White", "Rice Creamy"])
    selected_size = random.choice(["800g", "2.4kg"])
    simulated_qty = random.randint(10, 80)
    calculated_rev = simulated_qty * PRICE_BOOK[selected_size]
    
    # Verify current availability parameters
    if st.session_state.inventory[selected_rice][selected_size] >= simulated_qty:
        # Subtract stock allocation dynamically
        st.session_state.inventory[selected_rice][selected_size] -= simulated_qty
        
        # Build systematic JSON ledger record entry
        new_transaction = {
            "id": f"GRM-{random.randint(805, 999)}",
            "client": random.choice(["Hypermarket Grand", "Zayd Retailers", "Metro Food Hub", "Coastside Bistro", "Al-Amine Groceries"]),
            "type": selected_rice,
            "size": selected_size,
            "qty": simulated_qty,
            "revenue": calculated_rev,
            "status": "Processing",
            "lat": 33.8938 + random.uniform(-0.04, 0.04),
            "lon": 35.5018 + random.uniform(-0.04, 0.04),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        st.session_state.orders.insert(0, new_transaction)
        st.sidebar.success(f"Success! {selected_rice} ({selected_size}) ordered.")
    else:
        st.sidebar.error(f"Stockout Alert: Insufficient supply inventory for {selected_rice}!")

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Click the simulation button above repeatedly to build realistic operational data flows instantly.")

# ==============================================================================
# 4. HIGHEST LEVEL ANALYTICAL KPI BLOCKS (CEO SUMMARY STRIP)
# ==============================================================================
orders_df = pd.DataFrame(st.session_state.orders)
revenue_metric = orders_df["revenue"].sum()
units_metric = orders_df["qty"].sum()
active_logistics_count = len(orders_df[orders_df["status"].isin(["Processing", "Shipped", "In Transit"])])

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.markdown(f'<div class="metric-box"><h5>Gross Revenue Matrix</h5>🛑 <b>${revenue_metric:,.2f} USD</b></div>', unsafe_allow_html=True)
with kpi2:
    st.markdown(f'<div class="metric-box"><h5>Total Packaged Volumes Moving</h5>📦 <b>{units_metric:,} Bag Units</b></div>', unsafe_allow_html=True)
with kpi3:
    st.markdown(f'<div class="metric-box"><h5>Active Outbound Deliveries</h5>🚚 <b>{active_logistics_count} Transits Running</b></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 5. INVENTORY STOCK BALANCING ARCHITECTURE
# ==============================================================================
st.subheader("📦 Live Supply Chain Storage Ledger")

# Remap internal JSON state dictionary configurations to functional tabular structures
inventory_records = []
for product_variant, sizes_dict in st.session_state.inventory.items():
    for capacity_label, inventory_count in sizes_dict.items():
        inventory_records.append({
            "Rice Variety Line": product_variant,
            "Packaging Format": capacity_label,
            "Remaining Quantities (Units)": inventory_count
        })
rendered_inventory_df = pd.DataFrame(inventory_records)

# Generate comprehensive data visualization plot
visualization_chart = px.bar(
    rendered_inventory_df, 
    x="Rice Variety Line", 
    y="Remaining Quantities (Units)", 
    color="Packaging Format", 
    barmode="group",
    color_discrete_sequence=["#4caf50", "#ffb300"],
    title="Real-Time Warehouse Stock Availability Balance Charts"
)

layout_col_left, layout_col_right = st.columns([3, 2])
with layout_col_left:
    st.plotly_chart(visualization_chart, use_container_width=True)
with layout_col_right:
    st.markdown("**Stock Verification Matrix Data**")
    st.dataframe(rendered_inventory_df, hide_index=True, use_container_width=True)

st.markdown("---")

# ==============================================================================
# 6. GEOGRAPHIC FLEET DISPATCH MAP & BILLING DATA ACCESS LOGS
# ==============================================================================
st.subheader("📍 CEO Logistics Dispatch Tracker & Global Order Ledger")

layout_map_pane, layout_ledger_pane = st.columns([1, 1])

with layout_map_pane:
    st.markdown("**Live Delivery Route GPS Plots**")
    # Plot real map visualizations safely on screen
    st.map(orders_df, latitude="lat", longitude="lon", size=40)

with layout_ledger_pane:
    st.markdown("**Systematic Financial Ledger Logs & Receipt Controls**")
    
    # Loop over database indices explicitly to preserve state mutations dynamically
    for record_index in range(len(st.session_state.orders)):
        individual_order = st.session_state.orders[record_index]
        
        # Color match labels to design a high fidelity system visual
        status_badges = {"Delivered": "🟢", "In Transit": "🔵", "Shipped": "🟡", "Processing": "🟠"}
        badge = status_badges.get(individual_order["status"], "⚪")
        
        with st.expander(f"{badge} Receipt {individual_order['id']} — {individual_order['client']}"):
            st.markdown(f"**Transaction Timestamp:** `{individual_order['date']}`")
            st.markdown(f"**Item Line Formulation:** {individual_order['type']} ({individual_order['size']})")
            st.markdown(f"**Volume Dispatched:** {individual_order['qty']} unit bags")
            st.markdown(f"**Financial Settlements:** `${individual_order['revenue']:,.2f} USD`")
            st.markdown("---")
            
            # Interactive drop-down widget allowing users to adjust live business operations
            updated_status_selection = st.selectbox(
                "Modify Route Status Flags:",
                ["Processing", "Shipped", "In Transit", "Delivered"],
                index=["Processing", "Shipped", "In Transit", "Delivered"].index(individual_order["status"]),
                key=f"control_widget_key_{individual_order['id']}"
            )
            
            # Rerun layout elements immediately upon modification detection
            if updated_status_selection != individual_order["status"]:
                st.session_state.orders[record_index]["status"] = updated_status_selection
                st.toast(f"System status tracking update pushed: Invoice {individual_order['id']}")
                st.rerun()
