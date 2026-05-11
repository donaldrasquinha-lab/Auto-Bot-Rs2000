import streamlit as st
import plotly.graph_objects as go
import plotly.express as px  # Recommended to include this as well

from strategy import TradingStrategy
import pandas as pd

# Initialize Strategy
algo = TradingStrategy()

st.set_page_config(page_title="Deep ITM Algo Dashboard", layout="wide")

# Session State for Algo Toggle
if 'running' not in st.session_state: st.session_state.running = False

# --- SIDEBAR ---
with st.sidebar:
    st.title("Settings")
    token = st.text_input("Upstox Access Token", type="password")
    index_name = st.selectbox("Index", ["NIFTY", "BANKNIFTY"])
    expiry = st.date_input("Expiry Date")
    
    st.divider()
    if st.button("🔴 ACTIVATE KILL SWITCH", type="primary", use_container_width=True):
        st.session_state.running = False
        st.error("Emergency Exit Triggered: All Orders Cancelled.")
        # Add Upstox API call here: api.cancel_all_orders()

# --- MAIN DASHBOARD ---
col1, col2, col3 = st.columns(3)
with col1: st.metric("Index Spot", "24,150.20", "+0.45%")
with col2: st.metric("Upstox Margin", "₹1,42,000" if token else "Login Required")
with col3: st.metric("Live MTM", "₹0.00")

# --- CHART ---
st.subheader("Live Analysis")
# Simulated data for visual demonstration
df = pd.DataFrame({'close': [24100, 24120, 24115, 24130, 24150]})
df = algo.calculate_indicators(df)

fig = go.Figure()
fig.add_trace(go.Scatter(y=df['close'], name="Price", line=dict(color='white')))
fig.add_trace(go.Scatter(y=df['MA20'], name="20 MA", line=dict(color='red')))
fig.add_trace(go.Scatter(y=df['MA9'], name="9 MA", line=dict(color='blue')))
st.plotly_chart(fig, use_container_width=True)

# --- CONTROLS ---
c1, c2 = st.columns(2)
with c1:
    if st.button("Start Auto-Trade", use_container_width=True, disabled=not token):
        st.session_state.running = True
with c2:
    if st.button("Stop/Pause Algo", use_container_width=True):
        st.session_state.running = False

if st.session_state.running:
    st.success(f"Algorithm ACTIVE: Monitoring {index_name} for 20MA touch...")
    # Entry Logic Loop:
    # 1. Fetch live OHLC
    # 2. signal = algo.check_signal(df)
    # 3. if signal != "WAIT": strikes = algo.get_ladder_strikes(spot, signal) -> Execute!
else:
    st.info("Algorithm Status: Idle")
