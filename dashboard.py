import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import random

st.set_page_config(page_title="Bank Risk Dashboard", layout="wide")

st.title("🏦 Bank Risk Management Dashboard")

# Load Dow 20 close price data
@st.cache_data
def load_data():
    dow_tickers = [
        'AAPL', 'MSFT', 'JPM', 'BA', 'V', 'KO', 'MCD', 'IBM', 'HD', 'DIS',
        'GS', 'UNH', 'CAT', 'NKE', 'PG', 'CRM', 'MRK', 'WMT', 'AMGN', 'CSCO'
    ]
    raw_data = yf.download(dow_tickers, start='2023-01-01', end='2025-04-01')
    close_prices = raw_data.loc[:, 'Close']
    return close_prices

data = load_data()

# === Market Risk Calculations === #
daily_returns = data.pct_change().dropna()
weights = np.array([1/20] * 20)
portfolio_returns = daily_returns.dot(weights)

# Volatility & VaR
volatility = portfolio_returns.std() * np.sqrt(252)
VaR_95 = np.percentile(portfolio_returns, 5) * np.sqrt(252)

# Beta vs SPY
spy = yf.download('SPY', start='2023-01-01', end='2025-04-01')['Close']
spy_returns = spy.pct_change().dropna()
aligned = pd.concat([portfolio_returns, spy_returns], axis=1).dropna()
aligned.columns = ['Portfolio', 'SPY']
cov_matrix = np.cov(aligned['Portfolio'], aligned['SPY'])
beta = cov_matrix[0, 1] / cov_matrix[1, 1]

# Rolling volatility & drawdowns
rolling_volatility = portfolio_returns.rolling(window=30).std() * np.sqrt(252)
cumulative = (1 + portfolio_returns).cumprod()
rolling_max = cumulative.cummax()
drawdowns = (cumulative - rolling_max) / rolling_max

# === Layout & Visuals === #

st.markdown("### 📊 Market Risk Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Annualized Volatility", f"{volatility:.2%}")
col2.metric("95% Value at Risk (VaR)", f"{VaR_95:.2%}")
col3.metric("Beta vs SPY", f"{beta:.2f}")

# Cumulative returns chart
st.markdown("### 📈 Portfolio Performance")
cumulative_returns = (1 + portfolio_returns).cumprod() - 1
fig_cum = go.Figure()
fig_cum.add_trace(go.Scatter(
    x=cumulative_returns.index,
    y=cumulative_returns,
    mode='lines',
    name='Cumulative Returns'
))
fig_cum.update_layout(title="Portfolio Cumulative Return", xaxis_title="Date", yaxis_title="Return")
st.plotly_chart(fig_cum, use_container_width=True)

# Rolling Volatility and Drawdowns
st.markdown("### 📉 Rolling Volatility & Drawdowns")
col4, col5 = st.columns(2)

with col4:
    fig_vol = go.Figure()
    fig_vol.add_trace(go.Scatter(
        x=rolling_volatility.index,
        y=rolling_volatility,
        mode='lines',
        name='30-Day Rolling Volatility'
    ))
    fig_vol.update_layout(title="30-Day Rolling Volatility", xaxis_title="Date", yaxis_title="Volatility")
    st.plotly_chart(fig_vol, use_container_width=True)

with col5:
    fig_dd = go.Figure()
    fig_dd.add_trace(go.Scatter(
        x=drawdowns.index,
        y=drawdowns,
        mode='lines',
        name='Drawdown'
    ))
    fig_dd.update_layout(title="Portfolio Drawdowns", xaxis_title="Date", yaxis_title="Drawdown")
    st.plotly_chart(fig_dd, use_container_width=True)

# Mock data for enterprise risk types
st.markdown("### ⚠️ Other Risk Categories (Mock Data)")

mock_risks = {
    "Credit Risk": f"CDS Spread: {random.randint(90,130)} bps",
    "Operational Risk": f"Incidents Last Quarter: {random.randint(2,10)}",
    "Cybersecurity Risk": f"Threat Score: {random.randint(1,10)} / 10",
    "Compliance Risk": f"Open Issues: {random.randint(0,5)}",
    "Liquidity Risk": f"Liquidity Ratio: {round(random.uniform(1.5,3.0), 2)}",
    "Tech Risk": f"System Downtime: {round(random.uniform(0, 10), 1)} hrs",
    "Emerging Risk": f"ESG Score: {round(random.uniform(70,95), 1)}",
    "Geopolitical Risk": f"Exposures: USA, China, UK, Germany"
}

cols = st.columns(4)
for i, (risk, value) in enumerate(mock_risks.items()):
    cols[i % 4].info(f"**{risk}**\n\n{value}")

