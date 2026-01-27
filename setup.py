import os
import subprocess

# The Streamlit app code
app_code = '''import yfinance as yf
import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Commodity Tracker", page_icon="📊", layout="wide")

# Title
st.title("🌍 Global Commodity Tracker")

# Define commodities with nice names
commodities = {
    'CL=F': {'name': 'Crude Oil', 'emoji': '🛢️', 'unit': 'USD/barrel'},
    'GC=F': {'name': 'Gold', 'emoji': '🥇', 'unit': 'USD/oz'},
    'SI=F': {'name': 'Silver', 'emoji': '🥈', 'unit': 'USD/oz'},
    'HG=F': {'name': 'Copper', 'emoji': '🔶', 'unit': 'USD/lb'}
}

tickers = list(commodities.keys())

# Fetch data
with st.spinner('Fetching latest prices...'):
    # Get current and previous day data
    data = yf.download(tickers, period="5d", progress=False)
    
# Display commodity cards
cols = st.columns(4)

for idx, ticker in enumerate(tickers):
    with cols[idx]:
        info = commodities[ticker]
        
        # Get current and previous price
        current_price = data['Close'][ticker].iloc[-1]
        prev_price = data['Close'][ticker].iloc[-2]
        change = current_price - prev_price
        change_pct = (change / prev_price) * 100
        
        # Color based on change
        color = "green" if change >= 0 else "red"
        arrow = "▲" if change >= 0 else "▼"
        
        st.markdown(f"### {info['emoji']} {info['name']}")
        st.metric(
            label=info['unit'],
            value=f"${current_price:.2f}",
            delta=f"{change:+.2f} ({change_pct:+.2f}%)"
        )

# Show detailed data table
st.markdown("---")
st.subheader("📈 Detailed Price Data")

# Prepare nice display dataframe
display_data = pd.DataFrame()
for ticker in tickers:
    current_price = data['Close'][ticker].iloc[-1]
    prev_price = data['Close'][ticker].iloc[-2]
    change = current_price - prev_price
    change_pct = (change / prev_price) * 100
    
    display_data[commodities[ticker]['name']] = [
        f"${current_price:.2f}",
        f"{change:+.2f}",
        f"{change_pct:+.2f}%"
    ]

display_data.index = ['Current Price', 'Change ($)', 'Change (%)']
st.dataframe(display_data, use_container_width=True)

# Add refresh button
if st.button("🔄 Refresh Prices"):
    st.rerun()
'''

# Create the file
print("📝 Creating commodity_tracker.py...")
with open('commodity_tracker.py', 'w', encoding='utf-8') as f:
    f.write(app_code)

print("✅ File created successfully!")
print(f"📁 Location: {os.path.abspath('commodity_tracker.py')}")

# Install dependencies
print("\n📦 Installing dependencies...")
try:
    subprocess.run(['pip', 'install', 'yfinance', 'streamlit'], check=True)
    print("✅ Dependencies installed!")
except:
    print("⚠️ Could not install dependencies automatically.")
    print("Please run: pip install yfinance streamlit")

# Launch Streamlit
print("\n🚀 Launching Streamlit app...")
print("Press Ctrl+C to stop the server\n")
subprocess.run(['streamlit', 'run', 'commodity_tracker.py'])