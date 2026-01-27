import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="Commodity Tracker", page_icon="📊", layout="wide")

# Title
st.title("🌍 Global Asset Tracker")

# Define assets by category
commodities = {
    'GC=F': {'name': 'Gold', 'emoji': '🥇', 'unit': 'USD/oz'},
    'SI=F': {'name': 'Silver', 'emoji': '🥈', 'unit': 'USD/oz'},
    'HG=F': {'name': 'Copper', 'emoji': '🔶', 'unit': 'USD/lb'}
}

etfs = {
    'AIQ': {'name': 'Global X AI & Tech ETF', 'emoji': '🤖', 'unit': 'USD/share'},
    'SMH': {'name': 'VanEck Semiconductors', 'emoji': '💾', 'unit': 'USD/share'}
}

asian_markets = {
    '^KS11': {'name': 'South Korea KOSPI', 'emoji': '🇰🇷', 'unit': 'KOSPI'},
    '^TWII': {'name': 'Taiwan Weighted', 'emoji': '🇹🇼', 'unit': 'TWII'},
    '^JKSE': {'name': 'Jakarta Stock Exchange', 'emoji': '🇮🇩', 'unit': 'IDX'},
    '^NSEI': {'name': 'India Nifty 50', 'emoji': '🇮🇳', 'unit': 'NSEI'},
    '^STI': {'name': 'Singapore Straits Times', 'emoji': '🇸🇬', 'unit': 'STI'},
    '^KLSE': {'name': 'Malaysia KLSE', 'emoji': '🇲🇾', 'unit': 'KLSE'}
}

# Combine all tickers
all_assets = {**commodities, **etfs, **asian_markets}
tickers = list(all_assets.keys())

# Fetch current data
with st.spinner('Fetching latest prices...'):
    current_data = yf.download(tickers, period="5d", progress=False)

# Display by category - Commodities
st.subheader("💎 Commodities")
comm_cols = st.columns(3)

for idx, ticker in enumerate(commodities.keys()):
    with comm_cols[idx]:
        info = commodities[ticker]
        
        current_price = current_data['Close'][ticker].iloc[-1]
        prev_price = current_data['Close'][ticker].iloc[-2]
        change = current_price - prev_price
        change_pct = (change / prev_price) * 100
        
        st.markdown(f"<p style='font-size:14px; margin:0;'><strong>{info['emoji']} {info['name']}</strong></p>", unsafe_allow_html=True)
        st.metric(
            label=info['unit'],
            value=f"${current_price:.2f}",
            delta=f"{change:+.2f} ({change_pct:+.2f}%)",
            label_visibility="collapsed"
        )

# ETFs Section
st.subheader("📊 ETFs")
etf_cols = st.columns(2)

for idx, ticker in enumerate(etfs.keys()):
    with etf_cols[idx]:
        info = etfs[ticker]
        
        current_price = current_data['Close'][ticker].iloc[-1]
        prev_price = current_data['Close'][ticker].iloc[-2]
        change = current_price - prev_price
        change_pct = (change / prev_price) * 100
        
        st.markdown(f"<p style='font-size:14px; margin:0;'><strong>{info['emoji']} {info['name']}</strong></p>", unsafe_allow_html=True)
        st.metric(
            label=info['unit'],
            value=f"${current_price:.2f}",
            delta=f"{change:+.2f} ({change_pct:+.2f}%)",
            label_visibility="collapsed"
        )

# Asian Markets Section
st.subheader("🌏 Asian Markets")
asian_cols = st.columns(6)

for idx, ticker in enumerate(asian_markets.keys()):
    with asian_cols[idx]:
        info = asian_markets[ticker]
        
        current_price = current_data['Close'][ticker].iloc[-1]
        prev_price = current_data['Close'][ticker].iloc[-2]
        change = current_price - prev_price
        change_pct = (change / prev_price) * 100
        
        st.markdown(f"<p style='font-size:14px; margin:0;'><strong>{info['emoji']} {info['name']}</strong></p>", unsafe_allow_html=True)
        st.metric(
            label=info['unit'],
            value=f"{current_price:.2f}",
            delta=f"{change:+.2f} ({change_pct:+.2f}%)",
            label_visibility="collapsed"
        )

# Mini trend charts
st.markdown("---")
st.subheader("📈 Price Trends (Last 2 Years)")

with st.spinner('Loading 2-year trends...'):
    trend_data = yf.download(tickers, period="2y", progress=False)

# Commodities trends
st.markdown("**Commodities**")
comm_trend_cols = st.columns(3)

for idx, ticker in enumerate(commodities.keys()):
    with comm_trend_cols[idx]:
        info = commodities[ticker]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=trend_data.index,
            y=trend_data['Close'][ticker],
            mode='lines',
            line=dict(color='#00D9FF', width=2),
            fill='tozeroy',
            fillcolor='rgba(0, 217, 255, 0.1)',
            showlegend=False
        ))
        
        fig.update_layout(
            title=f"{info['emoji']} {info['name']}",
            height=250,
            margin=dict(l=10, r=10, t=40, b=30),
            xaxis=dict(showgrid=False, showticklabels=True),
            yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.2)'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ETFs trends
st.markdown("**ETFs**")
etf_trend_cols = st.columns(2)

for idx, ticker in enumerate(etfs.keys()):
    with etf_trend_cols[idx]:
        info = etfs[ticker]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=trend_data.index,
            y=trend_data['Close'][ticker],
            mode='lines',
            line=dict(color='#00D9FF', width=2),
            fill='tozeroy',
            fillcolor='rgba(0, 217, 255, 0.1)',
            showlegend=False
        ))
        
        fig.update_layout(
            title=f"{info['emoji']} {info['name']}",
            height=250,
            margin=dict(l=10, r=10, t=40, b=30),
            xaxis=dict(showgrid=False, showticklabels=True),
            yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.2)'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Asian Markets trends
st.markdown("**Asian Markets**")
asian_trend_cols = st.columns(3)

for idx, ticker in enumerate(asian_markets.keys()):
    with asian_trend_cols[idx % 3]:
        info = asian_markets[ticker]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=trend_data.index,
            y=trend_data['Close'][ticker],
            mode='lines',
            line=dict(color='#00D9FF', width=2),
            fill='tozeroy',
            fillcolor='rgba(0, 217, 255, 0.1)',
            showlegend=False
        ))
        
        fig.update_layout(
            title=f"{info['emoji']} {info['name']}",
            height=250,
            margin=dict(l=10, r=10, t=40, b=30),
            xaxis=dict(showgrid=False, showticklabels=True),
            yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.2)'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Show detailed data table
st.markdown("---")
st.subheader("📊 Detailed Price Data")

display_data = pd.DataFrame()
for ticker in tickers:
    current_price = current_data['Close'][ticker].iloc[-1]
    prev_price = current_data['Close'][ticker].iloc[-2]
    change = current_price - prev_price
    change_pct = (change / prev_price) * 100
    
    display_data[all_assets[ticker]['name']] = [
        f"${current_price:.2f}",
        f"{change:+.2f}",
        f"{change_pct:+.2f}%"
    ]

display_data.index = ['Current Price', 'Change ($)', 'Change (%)']
st.dataframe(display_data, use_container_width=True)

# Comparison chart - all assets normalized
st.markdown("---")
st.subheader("🔄 Normalized Price Comparison (% Change from 5 Years Ago)")

with st.spinner('Loading 5-year historical data...'):
    historical_data = yf.download(tickers, period="5y", progress=False)

fig_compare = go.Figure()

for ticker in tickers:
    info = all_assets[ticker]
    prices = historical_data['Close'][ticker]
    # Normalize to percentage change from first value
    normalized = ((prices / prices.iloc[0]) - 1) * 100
    
    fig_compare.add_trace(go.Scatter(
        x=historical_data.index,
        y=normalized,
        mode='lines',
        name=info['name'],
        line=dict(width=2)
    ))

fig_compare.update_layout(
    xaxis_title="Date",
    yaxis_title="% Change from Start",
    hovermode='x unified',
    height=500,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

st.plotly_chart(fig_compare, use_container_width=True)

# Add refresh button
if st.button("🔄 Refresh Prices"):
    st.rerun()