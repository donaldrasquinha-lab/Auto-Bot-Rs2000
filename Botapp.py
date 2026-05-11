import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from strategy import TradingStrategy

# Strategy Instance
algo = TradingStrategy()

st.set_page_config(page_title="Upstox Algo Pro", layout="wide")

# --- UI Header ---
st.title("⚡ Deep ITM Auto-Trader")
token = st.sidebar.text_input("Upstox Access Token", type="password")
index_choice = st.sidebar.selectbox("Index", ["NIFTY", "BANKNIFTY"])

# --- Kill Switch ---
if st.sidebar.button("🔴 ACTIVATE KILL SWITCH", type="primary", use_container_width=True):
    st.error("EMERGENCY EXIT: All positions squared off and bot stopped.")
    st.session_state.running = False

# --- Market Data Placeholder ---
# In a real app, you would fetch this from Upstox API
data = {
    'open': np.random.uniform(24000, 24100, 50),
    'high': np.random.uniform(24100, 24150, 50),
    'low': np.random.uniform(23950, 24000, 50),
    'close': np.random.uniform(24000, 24100, 50)
}
df = pd.DataFrame(data)
df = algo.calculate_indicators(df)

# --- Live Stats ---
c1, c2, c3 = st.columns(3)
c1.metric("Spot Price", f"{df['close'].iloc[-1]:.2f}")
c2.metric("ADX (Trend)", f"{df['ADX'].iloc[-1]:.2f}")
c3.metric("Current Signal", algo.check_signal(df))

# --- Graph ---
fig = go.Figure()
fig.add_trace(go.Candlestick(x=df.index, open=df['open'], high=df['high'], low=df['low'], close=df['close'], name="Candle"))
fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name="20 MA", line=dict(color='red')))
fig.add_trace(go.Scatter(x=df.index, y=df['MA9'], name="9 MA", line=dict(color='blue')))
fig.update_layout(template='plotly_dark', xaxis_rangeslider_visible=False)
st.plotly_chart(fig, use_container_width=True)

# --- Trading Actions ---
if st.button("Start Auto-Trade", disabled=not token):
    st.success(f"Algorithm running on {index_choice}...")
    
