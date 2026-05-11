import subprocess
import sys
import streamlit as st

# Temporary debug: Show installed packages
try:
    installed_packages = subprocess.check_output([sys.executable, "-m", "pip", "list"]).decode()
    st.sidebar.text_area("Installed Packages", installed_packages, height=200)
except:
    st.sidebar.write("Could not retrieve package list")

# Your original imports
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go



import streamlit as st
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime

# --- 1. Technical Analysis Logic ---
def get_indicators(df):
    df['EMA9'] = ta.ema(df['close'], length=9)
    df['EMA20'] = ta.ema(df['close'], length=20)
    return df

# --- 2. Plotly Graphing Function ---
def draw_chart(df):
    fig = go.Figure()

    # Candlestick Chart
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name='Market Price'
    ))

    # Add 9 EMA (Blue)
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA9'], 
                             line=dict(color='blue', width=1.5), 
                             name='9 EMA'))

    # Add 20 EMA (Red)
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], 
                             line=dict(color='red', width=1.5), 
                             name='20 EMA'))

    # Dark Theme Styling
    fig.update_layout(
        template='plotly_dark',
        xaxis_rangeslider_visible=False,
        title="Index Live Chart (9 & 20 EMA)",
        yaxis_title="Price"
    )
    
    return fig

# --- 3. Dashboard Display ---
st.title("Algo Trading Dashboard")

# Sample Data Placeholder
data = {
    'open': [24100, 24120, 24110, 24130, 24125],
    'high': [24130, 24140, 24120, 24150, 24140],
    'low': [24090, 24110, 24100, 24120, 24110],
    'close': [24120, 24110, 24115, 24140, 24135]
}
df = pd.DataFrame(data)
df = get_indicators(df)

# Show Chart
st.plotly_chart(draw_chart(df), use_container_width=True)
