import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page config
st.set_page_config(page_title="Commodity Tracker", page_icon="📊", layout="wide")

# Title
st.title("🌍 Global Asset Tracker")

# Technical Indicator Functions
def calculate_rsi(data, periods=14):
    """Calculate RSI"""
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(data, fast=12, slow=26, signal=9):
    """Calculate MACD"""
    exp1 = data.ewm(span=fast, adjust=False).mean()
    exp2 = data.ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line

def calculate_bollinger_bands(data, window=20, num_std=2):
    """Calculate Bollinger Bands"""
    sma = data.rolling(window=window).mean()
    std = data.rolling(window=window).std()
    upper_band = sma + (std * num_std)
    lower_band = sma - (std * num_std)
    return upper_band, sma, lower_band

def generate_signals(data, ticker_name):
    """Generate buy/sell signals based on technical indicators"""
    signals = []
    
    # Get latest values
    price = data['Close'].iloc[-1]
    rsi = data['RSI'].iloc[-1]
    macd = data['MACD'].iloc[-1]
    signal_line = data['Signal'].iloc[-1]
    upper_bb = data['BB_upper'].iloc[-1]
    lower_bb = data['BB_lower'].iloc[-1]
    sma_20 = data['SMA_20'].iloc[-1]
    sma_50 = data['SMA_50'].iloc[-1]
    
    # RSI signals
    if rsi < 30:
        signals.append("🟢 RSI Oversold - Potential BUY")
    elif rsi > 70:
        signals.append("🔴 RSI Overbought - Potential SELL")
    
    # MACD signals
    if macd > signal_line and data['MACD'].iloc[-2] <= data['Signal'].iloc[-2]:
        signals.append("🟢 MACD Bullish Crossover - BUY Signal")
    elif macd < signal_line and data['MACD'].iloc[-2] >= data['Signal'].iloc[-2]:
        signals.append("🔴 MACD Bearish Crossover - SELL Signal")
    
    # Bollinger Bands signals
    if price < lower_bb:
        signals.append("🟢 Price Below Lower BB - Potential BUY")
    elif price > upper_bb:
        signals.append("🔴 Price Above Upper BB - Potential SELL")
    
    # Moving Average signals
    if sma_20 > sma_50 and price > sma_20:
        signals.append("🟢 Golden Cross Pattern - BULLISH")
    elif sma_20 < sma_50 and price < sma_20:
        signals.append("🔴 Death Cross Pattern - BEARISH")
    
    if not signals:
        signals.append("⚪ HOLD - No strong signals")
    
    return signals

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
    '^JKSE': {'name': 'Jakarta Stock Exchange', 'emoji': '🇮🇩', 'unit': 'IDX'}
}

# Combine all tickers
all_assets = {**commodities, **etfs, **asian_markets}
tickers = list(all_assets.keys())

# Fetch current data
with st.spinner('Fetching latest prices...'):
    current_data = yf.download(tickers, period="5d", progress=False)

# Display all assets in one compact section
st.subheader("💎 Market Overview")

# Create columns for all assets (3 commodities + 2 ETFs + 3 Asian = 8 total)
all_cols = st.columns(8)

# Commodities
for idx, ticker in enumerate(commodities.keys()):
    with all_cols[idx]:
        info = commodities[ticker]
        
        current_price = current_data['Close'][ticker].iloc[-1]
        prev_price = current_data['Close'][ticker].iloc[-2]
        change = current_price - prev_price
        change_pct = (change / prev_price) * 100
        
        st.markdown(f"<p style='font-size:12px; margin:0;'><strong>{info['emoji']} {info['name']}</strong></p>", unsafe_allow_html=True)
        st.metric(
            label=info['unit'],
            value=f"${current_price:.2f}",
            delta=f"{change_pct:+.1f}%",
            label_visibility="collapsed"
        )

# ETFs
for idx, ticker in enumerate(etfs.keys()):
    with all_cols[idx + 3]:
        info = etfs[ticker]
        
        current_price = current_data['Close'][ticker].iloc[-1]
        prev_price = current_data['Close'][ticker].iloc[-2]
        change = current_price - prev_price
        change_pct = (change / prev_price) * 100
        
        st.markdown(f"<p style='font-size:12px; margin:0;'><strong>{info['emoji']} {info['name']}</strong></p>", unsafe_allow_html=True)
        st.metric(
            label=info['unit'],
            value=f"${current_price:.2f}",
            delta=f"{change_pct:+.1f}%",
            label_visibility="collapsed"
        )

# Asian Markets
for idx, ticker in enumerate(asian_markets.keys()):
    with all_cols[idx + 5]:
        info = asian_markets[ticker]
        
        current_price = current_data['Close'][ticker].iloc[-1]
        prev_price = current_data['Close'][ticker].iloc[-2]
        change = current_price - prev_price
        change_pct = (change / prev_price) * 100
        
        st.markdown(f"<p style='font-size:12px; margin:0;'><strong>{info['emoji']} {info['name']}</strong></p>", unsafe_allow_html=True)
        st.metric(
            label=info['unit'],
            value=f"{current_price:.2f}",
            delta=f"{change_pct:+.1f}%",
            label_visibility="collapsed"
        )

# Show detailed data table
st.markdown("---")
st.subheader("📊 Detailed Price Data")

# Fetch additional historical data for comparisons with more buffer
with st.spinner('Fetching historical data...'):
    hist_1m = yf.download(tickers, period="2mo", progress=False)
    hist_3m = yf.download(tickers, period="6mo", progress=False)
    hist_ytd = yf.download(tickers, period="ytd", progress=False)
    hist_1y = yf.download(tickers, period="2y", progress=False)

display_data = pd.DataFrame()

for ticker in tickers:
    current_price = current_data['Close'][ticker].iloc[-1]
    prev_price = current_data['Close'][ticker].iloc[-2]
    
    change = current_price - prev_price
    change_pct = (change / prev_price) * 100
    
    # WoW - get price from approximately 7 days ago
    try:
        if len(hist_1m['Close'][ticker]) > 5:
            price_1w_ago = hist_1m['Close'][ticker].iloc[min(5, len(hist_1m['Close'][ticker])-1)]
        else:
            price_1w_ago = hist_1m['Close'][ticker].iloc[0]
        wow_change = ((current_price - price_1w_ago) / price_1w_ago) * 100
    except:
        wow_change = 0
    
    # MoM - get price from approximately 30 days ago
    try:
        if len(hist_1m['Close'][ticker]) > 20:
            price_1m_ago = hist_1m['Close'][ticker].iloc[min(20, len(hist_1m['Close'][ticker])-1)]
        else:
            price_1m_ago = hist_1m['Close'][ticker].iloc[0]
        mom_change = ((current_price - price_1m_ago) / price_1m_ago) * 100
    except:
        mom_change = 0
    
    # QoQ - get price from approximately 90 days ago
    try:
        if len(hist_3m['Close'][ticker]) > 60:
            price_3m_ago = hist_3m['Close'][ticker].iloc[min(60, len(hist_3m['Close'][ticker])-1)]
        else:
            price_3m_ago = hist_3m['Close'][ticker].iloc[0]
        qoq_change = ((current_price - price_3m_ago) / price_3m_ago) * 100
    except:
        qoq_change = 0
    
    # YTD
    try:
        price_ytd = hist_ytd['Close'][ticker].iloc[0]
        ytd_change = ((current_price - price_ytd) / price_ytd) * 100
    except:
        ytd_change = 0
    
    # YoY - get price from approximately 252 days ago (1 year trading days)
    try:
        if len(hist_1y['Close'][ticker]) > 252:
            price_1y_ago = hist_1y['Close'][ticker].iloc[min(252, len(hist_1y['Close'][ticker])-1)]
        else:
            price_1y_ago = hist_1y['Close'][ticker].iloc[0]
        yoy_change = ((current_price - price_1y_ago) / price_1y_ago) * 100
    except:
        yoy_change = 0
    
    display_data[all_assets[ticker]['name']] = [
        current_price,
        change_pct,
        wow_change,
        mom_change,
        qoq_change,
        ytd_change,
        yoy_change
    ]

display_data.index = ['Current Price', 'Change (%)', 'WoW %', 'MoM %', 'QoQ %', 'YTD %', 'YoY %']

# Style and display the table with gradient colors
def get_color_gradient(val):
    """Get color based on value with gradient effect - full spectrum every 5%"""
    if val >= 50:
        return '#004d00'  # Darkest green
    elif val >= 45:
        return '#005a00'
    elif val >= 40:
        return '#006600'
    elif val >= 35:
        return '#007300'
    elif val >= 30:
        return '#008000'  # Green
    elif val >= 25:
        return '#009900'
    elif val >= 20:
        return '#00b300'
    elif val >= 15:
        return '#00cc00'
    elif val >= 10:
        return '#00e600'
    elif val >= 5:
        return '#00ff00'  # Bright green
    elif val > 0:
        return '#90EE90'  # Light green
    elif val == 0:
        return '#e0e0e0'  # Light gray
    elif val > -5:
        return '#ffcccc'  # Light red
    elif val > -10:
        return '#ff9999'
    elif val > -15:
        return '#ff6666'
    elif val > -20:
        return '#ff3333'
    elif val > -25:
        return '#ff0000'  # Bright red
    elif val > -30:
        return '#e60000'
    elif val > -35:
        return '#cc0000'
    elif val > -40:
        return '#b30000'
    elif val > -45:
        return '#990000'
    elif val > -50:
        return '#800000'
    else:
        return '#660000'  # Darkest red

def style_value(val, row_name):
    if row_name == 'Current Price':
        return f'${val:.2f}'
    else:
        color = get_color_gradient(val)
        text_color = 'white' if abs(val) >= 5 else 'black'
        return f'<span style="background-color: {color}; color: {text_color}; padding: 2px 8px; border-radius: 4px; font-weight: bold;">{val:+.2f}%</span>'

# Create HTML table
html_rows = []
for idx in display_data.index:
    row_html = f'<tr><td style="font-weight: bold; padding: 8px;">{idx}</td>'
    for col in display_data.columns:
        val = display_data.at[idx, col]
        styled_val = style_value(val, idx)
        row_html += f'<td style="padding: 8px; text-align: center;">{styled_val}</td>'
    row_html += '</tr>'
    html_rows.append(row_html)

header_html = '<tr style="background-color: #f0f0f0;"><th style="padding: 8px;"></th>' + ''.join([f'<th style="padding: 8px; text-align: center;">{col}</th>' for col in display_data.columns]) + '</tr>'
table_html = f'''
<style>
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    th {{
        background-color: #f0f0f0;
        font-weight: bold;
    }}
    tr:nth-child(even) {{
        background-color: #f9f9f9;
    }}
    tr:hover {{
        background-color: #f5f5f5;
    }}
</style>
<table>
    {header_html}
    {"".join(html_rows)}
</table>
'''

st.markdown(table_html, unsafe_allow_html=True)

# Technical Analysis Section
st.markdown("---")
st.subheader("📈 Technical Analysis & Signals (Last 2 Years)")

with st.spinner('Calculating technical indicators...'):
    trend_data = yf.download(tickers, period="2y", progress=False)
    
    # Calculate indicators for each ticker
    technical_data = {}
    for ticker in tickers:
        df = pd.DataFrame()
        df['Close'] = trend_data['Close'][ticker]
        
        # Calculate indicators
        df['RSI'] = calculate_rsi(df['Close'])
        df['MACD'], df['Signal'] = calculate_macd(df['Close'])
        df['BB_upper'], df['BB_middle'], df['BB_lower'] = calculate_bollinger_bands(df['Close'])
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        
        technical_data[ticker] = df

# Commodities trends with indicators
st.markdown("**Commodities**")
for ticker in commodities.keys():
    info = commodities[ticker]
    data = technical_data[ticker]
    
    # Generate signals
    signals = generate_signals(data, info['name'])
    
    # Create subplot with price and RSI
    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.7, 0.3],
        subplot_titles=(f"{info['emoji']} {info['name']}", "RSI"),
        vertical_spacing=0.1
    )
    
    # Price chart with Bollinger Bands
    fig.add_trace(go.Scatter(x=data.index, y=data['BB_upper'], 
                             name='BB Upper', line=dict(color='rgba(250,128,114,0.3)', width=1),
                             showlegend=False), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data['BB_lower'], 
                             name='BB Lower', line=dict(color='rgba(250,128,114,0.3)', width=1),
                             fill='tonexty', fillcolor='rgba(250,128,114,0.1)',
                             showlegend=False), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], 
                             name='Price', line=dict(color='#00D9FF', width=2)), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], 
                             name='SMA 20', line=dict(color='orange', width=1, dash='dash')), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], 
                             name='SMA 50', line=dict(color='red', width=1, dash='dash')), row=1, col=1)
    
    # RSI
    fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], 
                             name='RSI', line=dict(color='purple', width=2)), row=2, col=1)
    fig.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.5, row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.5, row=2, col=1)
    
    fig.update_layout(height=500, hovermode='x unified', showlegend=True)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(title_text=info['unit'], row=1, col=1)
    fig.update_yaxes(title_text="RSI", row=2, col=1)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display signals
    st.markdown("**Trading Signals:**")
    for signal in signals:
        st.markdown(f"- {signal}")
    st.markdown("---")

# ETFs trends with indicators
st.markdown("**ETFs**")
for ticker in etfs.keys():
    info = etfs[ticker]
    data = technical_data[ticker]
    
    signals = generate_signals(data, info['name'])
    
    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.7, 0.3],
        subplot_titles=(f"{info['emoji']} {info['name']}", "RSI"),
        vertical_spacing=0.1
    )
    
    fig.add_trace(go.Scatter(x=data.index, y=data['BB_upper'], 
                             name='BB Upper', line=dict(color='rgba(250,128,114,0.3)', width=1),
                             showlegend=False), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data['BB_lower'], 
                             name='BB Lower', line=dict(color='rgba(250,128,114,0.3)', width=1),
                             fill='tonexty', fillcolor='rgba(250,128,114,0.1)',
                             showlegend=False), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], 
                             name='Price', line=dict(color='#00D9FF', width=2)), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], 
                             name='SMA 20', line=dict(color='orange', width=1, dash='dash')), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], 
                             name='SMA 50', line=dict(color='red', width=1, dash='dash')), row=1, col=1)
    
    fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], 
                             name='RSI', line=dict(color='purple', width=2)), row=2, col=1)
    fig.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.5, row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.5, row=2, col=1)
    
    fig.update_layout(height=500, hovermode='x unified', showlegend=True)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(title_text=info['unit'], row=1, col=1)
    fig.update_yaxes(title_text="RSI", row=2, col=1)
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("**Trading Signals:**")
    for signal in signals:
        st.markdown(f"- {signal}")
    st.markdown("---")

# Asian Markets trends with indicators
st.markdown("**Asian Markets**")
for ticker in asian_markets.keys():
    info = asian_markets[ticker]
    data = technical_data[ticker]
    
    signals = generate_signals(data, info['name'])
    
    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.7, 0.3],
        subplot_titles=(f"{info['emoji']} {info['name']}", "RSI"),
        vertical_spacing=0.1
    )
    
    fig.add_trace(go.Scatter(x=data.index, y=data['BB_upper'], 
                             name='BB Upper', line=dict(color='rgba(250,128,114,0.3)', width=1),
                             showlegend=False), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data['BB_lower'], 
                             name='BB Lower', line=dict(color='rgba(250,128,114,0.3)', width=1),
                             fill='tonexty', fillcolor='rgba(250,128,114,0.1)',
                             showlegend=False), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], 
                             name='Price', line=dict(color='#00D9FF', width=2)), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], 
                             name='SMA 20', line=dict(color='orange', width=1, dash='dash')), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], 
                             name='SMA 50', line=dict(color='red', width=1, dash='dash')), row=1, col=1)
    
    fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], 
                             name='RSI', line=dict(color='purple', width=2)), row=2, col=1)
    fig.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.5, row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.5, row=2, col=1)
    
    fig.update_layout(height=500, hovermode='x unified', showlegend=True)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(title_text=info['unit'], row=1, col=1)
    fig.update_yaxes(title_text="RSI", row=2, col=1)
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("**Trading Signals:**")
    for signal in signals:
        st.markdown(f"- {signal}")
    st.markdown("---")

# Comparison chart
st.markdown("---")
st.subheader("🔄 Normalized Price Comparison (% Change from 5 Years Ago)")

with st.spinner('Loading 5-year historical data...'):
    historical_data = yf.download(tickers, period="5y", progress=False)

fig_compare = go.Figure()

for ticker in tickers:
    info = all_assets[ticker]
    prices = historical_data['Close'][ticker]
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
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_compare, use_container_width=True)

if st.button("🔄 Refresh Prices"):
    st.rerun()