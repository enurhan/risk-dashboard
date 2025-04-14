import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import random
import plotly.express as px


st.set_page_config(page_title="Bank Risk Dashboard", layout="wide")

# === Sidebar Info ===
with st.sidebar:
    st.title("🧠 About")
    st.markdown("""
    **Bank Risk Dashboard**

    This tool analyzes market and enterprise risks across a Dow 20 equity portfolio.
    
    **Built by:** Ekrem Nurhan  
    [GitHub](https://github.com/enurhan)  
    <a href="https://www.linkedin.com/in/ekrem-nurhan-2b395b67" target="_blank">LinkedIn</a>
""", unsafe_allow_html=True)
    st.caption("Powered by Streamlit + yFinance")

# === Load Data ===
@st.cache_data
def load_data():
    tickers = [
        'AAPL', 'MSFT', 'JPM', 'BA', 'V', 'KO', 'MCD', 'IBM', 'HD', 'DIS',
        'GS', 'UNH', 'CAT', 'NKE', 'PG', 'CRM', 'MRK', 'WMT', 'AMGN', 'CSCO'
    ]
    data = yf.download(tickers, start="2023-01-01", end="2024-12-31", auto_adjust=True, group_by="ticker")
    return data

data = load_data()

# === Extract Close Prices ===
try:
    close_prices = pd.DataFrame({ticker: data[ticker]['Close'] for ticker in data.columns.levels[0]})
except Exception:
    st.error("❌ Failed to extract 'Close' prices from the data.")
    st.stop()

returns = close_prices.pct_change().dropna()
weights = np.array([1/20] * 20)  # Equal weights
portfolio_returns = returns.dot(weights)

# === Safety Checks ===
if close_prices.empty or returns.empty or portfolio_returns.empty:
    st.error("❌ Data failed to load. Try refreshing or check internet connection.")
    st.stop()

# === Risk Metrics ===
volatility = portfolio_returns.std() * np.sqrt(252)

try:
    VaR_95 = np.percentile(portfolio_returns, 5) * np.sqrt(252)
    VaR_99 = np.percentile(portfolio_returns, 1) * np.sqrt(252)
except:
    VaR_95 = VaR_99 = 0
    st.warning("⚠️ VaR unavailable due to insufficient data.")

try:
    spy = yf.download('SPY', start="2023-01-01", end="2024-12-31", auto_adjust=True)['Close']
    spy_returns = spy.pct_change().dropna()
    aligned = pd.concat([portfolio_returns, spy_returns], axis=1).dropna()
    aligned.columns = ['Portfolio', 'SPY']
    beta = np.cov(aligned['Portfolio'], aligned['SPY'])[0, 1] / np.var(aligned['SPY'])
except:
    beta = 0
    st.warning("⚠️ Beta unavailable due to SPY data issue.")

# === Gauges ===
def gauge_chart(title, value, min_val, max_val, suffix=""):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={'suffix': suffix},
        title={'text': title, 'font': {'size': 16}},
        gauge={
            'axis': {'range': [min_val, max_val]},
            'bar': {'color': "#1f77b4"},
        }
    ))
    fig.update_layout(
        height=280,
        margin=dict(t=40, b=0, l=0, r=0),
    )
    return fig


st.markdown("<h1 style='text-align: center;'>Risk Dashboard</h1>", unsafe_allow_html=True)







# === Executive Overview ===
st.markdown("## Executive Overview")

col1, col2, col3 = st.columns([1.2, 1, 1])

# --- Left Column: Risk Heatmap ---
with col1:
    st.markdown("### 🔥 Risk Category Heatmap")

    risk_categories = {
        "Credit Risk": random.choice(["Low", "Medium", "High"]),
        "Liquidity Risk": random.choice(["Low", "Medium", "High"]),
        "Operational Risk": random.choice(["Low", "Medium", "High"]),
        "Cybersecurity Risk": random.choice(["Low", "Medium", "High"]),
        "Compliance Risk": random.choice(["Low", "Medium", "High"]),
        "Legal Risk": random.choice(["Low", "Medium", "High"]),
        "Tech Risk": random.choice(["Low", "Medium", "High"]),
        "Geopolitical Risk": random.choice(["Low", "Medium", "High"]),
        "Emerging Risk": random.choice(["Low", "Medium", "High"]),
    }

    def risk_color(level):
        return {
            "Low": "🟢",
            "Medium": "🟡",
            "High": "🔴"
        }[level]

    heatmap_data = pd.DataFrame([
        {"Risk Type": k, "Severity": risk_color(v) + " " + v} for k, v in risk_categories.items()
    ])
    st.dataframe(heatmap_data, use_container_width=True, hide_index=True)

# --- Middle Column: Overall Risk Health Gauge ---
with col2:
    st.markdown("### 🧪 Risk Health Score")

    health_score = random.randint(0, 100)  # Simulated score

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=health_score,
        number={'suffix': " / 100"},
        title={'text': "Overall Health"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 33], 'color': "green"},
                {'range': [33, 66], 'color': "yellow"},
                {'range': [66, 100], 'color': "red"},
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': health_score
            }
        }
    ))

    fig.update_layout(height=270, margin=dict(t=10, b=0))
    st.plotly_chart(fig, use_container_width=True)



# --- Right Column: Limit Traffic Lights ---
with col3:
    st.markdown("### 🚦 Risk Appetite")

    limits = {
        "VaR Limit": random.choice(["Green", "Yellow", "Red"]),
        "Liquidity Ratio": random.choice(["Green", "Yellow", "Red"]),
        "Counterparty Exposure": random.choice(["Green", "Yellow", "Red"]),
    }

    def color_square(status):
        return {
            "Green": "🟢",
            "Yellow": "🟡",
            "Red": "🔴"
        }[status]

    for metric, status in limits.items():
        st.markdown(f"**{color_square(status)} {metric}**")





# === Risk Category Drilldowns ===
st.markdown("## Risk Category Drilldowns")

tabs = st.tabs([
    "Credit Risk",  "Cybersecurity Risk",  "Operational Risk",
    "Compliance Risk",  "Liquidity Risk",  "Tech Risk", 
    "Geopolitical Risk",  "Emerging Risk"
])

risk_descriptions = {
    "Credit Risk": "Exposure to counterparty defaults or credit spread widening.",
    "Cybersecurity Risk": "Threats from data breaches, ransomware, or system compromise.",
    "Operational Risk": "Risk of loss from failed processes, people, or systems.",
    "Compliance Risk": "Violations of laws, regulations, or internal policies.",
    "Liquidity Risk": "Inability to meet obligations without significant loss.",
    "Tech Risk": "Failures in IT systems, applications, or data infrastructure.",
    "Geopolitical Risk": "Instability due to political, war, or sanctions events.",
    "Emerging Risk": "New or evolving risks (e.g., AI misuse, climate transition)."
}

for tab, label in zip(tabs, risk_descriptions.keys()):
    with tab:
    
        if label == "Credit Risk":
            with st.expander("📉 Credit Risk – Click to expand / collapse", expanded=False):
                st.subheader("📈 Corporate CDS Spread (bps)")

                cds_dates = pd.date_range(end=pd.Timestamp.today(), periods=30)
                cds_spread = np.random.normal(loc=80, scale=10, size=30).clip(50, 150)

                cds_df = pd.DataFrame({
                     "Date": cds_dates,
                     "CDS Spread (bps)": cds_spread
        })

                st.line_chart(cds_df.set_index("Date"))

                st.markdown("---")
                st.subheader("🏦 Top 5 Counterparties by Exposure")

                counterparty_data = {
                    "Counterparty": ["JPM", "GS", "P72", "Citi", "Softbank"],
                    "Exposure ($M)": [120, 95, 88, 73, 60],
                    "Rating": ["A-", "BBB+", "BB", "A", "BBB"]
                }

                counterparty_df = pd.DataFrame(counterparty_data)
                st.dataframe(counterparty_df)

                st.markdown("---")
                st.subheader("📈 Risk Score Over Time")

                score_data = pd.DataFrame({
                    "Date": pd.date_range(end=pd.Timestamp.today(), periods=30),
                    "Risk Score": np.random.normal(6, 1, size=30).clip(1, 10)
                })

                # Format dates to dd/mm
                score_data["Date"] = score_data["Date"].dt.strftime("%d/%m")

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=score_data["Date"], y=score_data["Risk Score"], mode="lines+markers"))
                fig.update_layout(
                    xaxis_title="Date (dd/mm)",
                    yaxis_title="Score",
                    margin=dict(t=20, b=20),
                    height=300
                )

                st.plotly_chart(fig, use_container_width=True)


                st.info("⚠️ Watchlist: 2 counterparties flagged for monitoring due to rising CDS spreads.")


        elif label == "Cybersecurity Risk":
            with st.expander("🛡️ Cybersecurity Risk – Click to expand / collapse", expanded=False):
                st.subheader("🛡️ Threat Level (0–100)")

                threat_score = random.randint(20, 95)

                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=threat_score,
                    number={'suffix': " / 100"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "black"},
                        'steps': [
                            {'range': [0, 33], 'color': "green"},
                            {'range': [33, 66], 'color': "yellow"},
                            {'range': [66, 100], 'color': "red"},
                        ],
                        'threshold': {
                            'line': {'color': "black", 'width': 4},
                            'value': threat_score
                        }
                    }
                ))

                fig.update_layout(height=250, margin=dict(t=10, b=10))
                st.plotly_chart(fig, use_container_width=True)

                if threat_score > 70:
                    st.error("🚨 High threat level! Review all active incidents immediately.")

                st.markdown("---")
                st.subheader("📅 Recent Incidents (Last 30 Days)")

                incidents = pd.DataFrame({
                    "Date": pd.date_range(end=pd.Timestamp.today(), periods=5),
                    "Event": [
                        "Phishing attempt flagged",
                        "Malware blocked by endpoint",
                        "Suspicious login from unknown device",
                        "Firewall rule triggered",
                        "Unauthorized access to shared drive"
                    ],
                    "Status": ["Investigating", "Resolved", "Investigating", "Resolved", "Escalated"]
                })

                st.dataframe(incidents)

                st.markdown("---")
                st.subheader("📊 Attack Volume (Simulated)")

                attack_volume = pd.DataFrame({
                    "Date": pd.date_range(end=pd.Timestamp.today(), periods=30),
                    "Alerts": np.random.poisson(5, 30)
                })

                st.bar_chart(attack_volume.set_index("Date"))


        elif label == "Operational Risk":
            with st.expander("⚙️ Operational Risk – Click to expand / collapse", expanded=False):
                st.subheader("⚙️ Incident Count by Category")

                categories = ["Process Failure", "System Outage", "Human Error", "Third-Party", "Fraud"]
                incidents = np.random.randint(1, 15, size=len(categories))

                category_df = pd.DataFrame({
                    "Category": categories,
                    "Incidents": incidents
                })

                st.bar_chart(category_df.set_index("Category"))

                st.markdown("---")
                st.subheader("📅 Recent Operational Events")

                op_events = pd.DataFrame({
                    "Date": pd.date_range(end=pd.Timestamp.today(), periods=5),
                    "Event": [
                        "Payment system outage (2h)",
                        "Incorrect NAV calculation",
                        "Trade reconciliation error",
                        "Cloud sync failure",
                        "Vendor SLA breach"
                    ],
                    "Status": ["Resolved", "Investigating", "Resolved", "Monitoring", "Escalated"]
                })

                st.dataframe(op_events)

                st.markdown("---")
                st.subheader("🔒 Control Effectiveness Matrix")

                controls_df = pd.DataFrame({
                    "Control": ["Access Management", "Data Reconciliation", "Backup Procedures", "Incident Response"],
                    "Status": ["Good", "Needs Review", "Good", "At Risk"]
                })

                st.dataframe(controls_df)

                if sum(incidents) > 40:
                    st.warning("⚠️ Spike in operational incidents. Immediate review recommended.")


        elif label == "Compliance Risk":
            with st.expander("⚖️ Compliance Risk – Click to expand / collapse", expanded=False):
                st.subheader("⚠️ Compliance Violations Breakdown")

                issue_types = ["KYC/AML", "Trade Reporting", "Insider Trading", "Disclosure", "Privacy"]
                issue_counts = np.random.randint(1, 15, size=len(issue_types))

                issue_df = pd.DataFrame({
                    "Type": issue_types,
                    "Count": issue_counts
                })

                fig = px.pie(issue_df, names="Type", values="Count", title="Violations by Type")
                st.plotly_chart(fig, use_container_width=True)

                st.markdown("---")
                st.subheader("📋 Overdue Training (Sample)")

                training_df = pd.DataFrame({
                    "Employee": ["Alice Smith", "John Doe", "Eva Zhang", "Carlos Reyes", "Sarah Patel"],
                    "Training": ["AML Refresher", "Market Conduct", "Data Privacy", "Code of Ethics", "KYC Basics"],
                    "Due Date": pd.date_range(end=pd.Timestamp.today(), periods=5).strftime("%d/%m/%Y"),
                    "Status": ["Overdue", "Overdue", "Completed", "Overdue", "Completed"]
                })

                st.dataframe(training_df)

                st.markdown("---")
                st.subheader("📑 Policy Exceptions")

                exceptions_df = pd.DataFrame({
                    "Policy": ["Expense Reporting", "Trade Pre-Clearance", "Gift Limits"],
                    "# of Exceptions": [3, 5, 2],
                    "Review Status": ["Pending", "Under Review", "Closed"]
                })

                # Convert to HTML with style
                html_table = exceptions_df.to_html(index=False, classes='styled-table')

                # Custom styling: black header, white font
                st.markdown("""
                <style>
                .styled-table {
                    width: 100%;
                    border-collapse: collapse;
                    font-size: 16px;
                    font-family: sans-serif;
                }
                .styled-table th {
                    background-color: black;
                    color: white;
                    padding: 8px;
                    text-align: center;
                }
                .styled-table td {
                    border: 
                    padding: 8px;
                    text-align: center;
                }
                </style>
                """, unsafe_allow_html=True)

                # Render the styled table
                st.markdown(html_table, unsafe_allow_html=True)





                if sum(issue_counts) > 30:
                    st.warning("⚠️ High volume of compliance issues. Regulatory risk elevated.")

        
        elif label == "Liquidity Risk":
            with st.expander("💧 Liquidity Risk – Click to expand / collapse", expanded=False):
                st.subheader("💧 Liquidity Coverage Ratio (LCR) – Last 30 Days")

                lcr_data = pd.DataFrame({
                    "Date": pd.date_range(end=pd.Timestamp.today(), periods=30),
                    "LCR (%)": np.random.normal(115, 10, size=30).clip(70, 140)
                })

                st.line_chart(lcr_data.set_index("Date"))

                latest_lcr = lcr_data["LCR (%)"].iloc[-1]
                if latest_lcr < 100:
                    st.error(f"⚠️ LCR has dropped below regulatory threshold! Current: {latest_lcr:.1f}%")

                st.markdown("---")
                st.subheader("🏦 Cash Buffer by Currency (Mock)")

                cash_df = pd.DataFrame({
                    "Currency": ["USD", "EUR", "GBP", "JPY", "CHF"],
                    "Cash Available ($M)": [850, 430, 220, 310, 140]
                })

                st.bar_chart(cash_df.set_index("Currency"))

                st.markdown("---")
                st.subheader("📊 Liquidity Stress Test (Simulated)")

                stress_df = pd.DataFrame({
                    "Scenario": ["Base Case", "Mild Outflow", "Severe Outflow", "Extreme Stress"],
                    "Liquidity Gap ($M)": [0, -120, -300, -580]
                })

                st.dataframe(stress_df)

        elif label == "Tech Risk":
            with st.expander("💻 Tech Risk – Click to expand / collapse", expanded=False):
                st.subheader("💻 System Uptime (Rolling 30 Days)")

                uptime_data = pd.DataFrame({
                    "Date": pd.date_range(end=pd.Timestamp.today(), periods=30),
                    "Uptime %": np.random.normal(99.7, 0.2, size=30).clip(98.5, 100)
                })

                st.line_chart(uptime_data.set_index("Date"))

                if uptime_data["Uptime %"].iloc[-1] < 99:
                    st.warning("⚠️ Uptime has dipped below SLA threshold!")

                st.markdown("---")
                st.subheader("🔧 Critical System Incidents (Past Month)")

                incidents_df = pd.DataFrame({
                    "Date": pd.date_range(end=pd.Timestamp.today(), periods=5),
                    "System": ["Order Mgmt", "Risk Engine", "Trading API", "CRM", "Data Warehouse"],
                    "Impact": ["High", "Medium", "High", "Low", "Medium"],
                    "Status": ["Resolved", "Monitoring", "Escalated", "Resolved", "Resolved"]
                })

                st.dataframe(incidents_df)

                st.markdown("---")
                st.subheader("🛠️ DevOps Deployment Stats")

                devops_df = pd.DataFrame({
                    "Metric": ["Deploys", "Rollback %", "Hotfixes", "Failed Jobs"],
                    "Value": [42, "2%", 5, 3]
                })

                st.dataframe(devops_df)


        elif label == "Geopolitical Risk":
            with st.expander("🌍 Geopolitical Risk – Click to expand / collapse", expanded=False):
                st.subheader("🌍 Global Hotspots – Country Watchlist")

                country_df = pd.DataFrame({
                    "Country": ["Ukraine", "China", "Iran", "Venezuela", "South Sudan"],
                    "Risk Score": [9.5, 8.2, 7.8, 6.9, 6.5],
                    "Event": ["War", "Tarriffs", "Sanctions", "Political Unrest", "Oil Conflict"]
                })

                st.dataframe(country_df)

                st.markdown("---")
                st.subheader("🧭 Regional Exposure (Mock %)")

                exposure_df = pd.DataFrame({
                    "Region": ["North America", "Europe", "Asia", "Middle East", "South America"],
                    "Exposure (%)": [40, 25, 15, 10, 10]
                })

                fig = px.pie(exposure_df, names="Region", values="Exposure (%)", title="Portfolio Regional Exposure")
                st.plotly_chart(fig, use_container_width=True)

                st.markdown("---")
                st.subheader("📰 Real-Time Headlines (Static for now)")

                headlines = [
                    "⚠️ Missile strike near key pipeline in Ukraine",
                    "🇨🇳 Tarrifs with China",
                    "🛢️ Oil sanctions expected to tighten global supply",
                    "📉 Emerging market debt spreads widen amid unrest"
                ]
                for headline in headlines:
                    st.write(headline)


        elif label == "Emerging Risk":
            with st.expander("🚀 Emerging Risk – Click to expand / collapse", expanded=False):
                st.subheader("🚀 Risk Radar – Emerging Themes")

                radar_df = pd.DataFrame({
                    "Risk": ["AI Ethics", "Quantum Risk", "Climate Litigation", "ESG Data Gaps", "Decentralized Finance"],
                    "Score (1–10)": np.random.randint(3, 10, size=5)
                })

                fig = px.bar(radar_df, x="Risk", y="Score (1–10)", color="Score (1–10)", title="Emerging Risk Ratings")
                st.plotly_chart(fig, use_container_width=True)

                st.markdown("---")
                st.subheader("🔍 Key Monitoring Notes")

                notes = [
                    "- AI hallucination risk flagged in fraud detection models",
                    "- Early climate lawsuits filed in EU courts",
                    "- SEC guidance pending on DeFi regulatory scope",
                    "- ESG vendor data discrepancies impacting scoring"
                ]
                for note in notes:
                    st.markdown(f"• {note}")

                st.markdown("---")
                st.info("💡 Emerging risks are monitored weekly by the Innovation Risk Committee.")

# === Portfolio Return Plot ===
st.markdown("## Risk Analytics")
with st.expander("📊 Risk Analytics - Click to expand / collapse", expanded=False):
    # 1. 📉 Max Drawdown Chart
    st.subheader("📉 Portfolio Max Drawdown (Rolling 30 Days)")

    cumulative_returns = (1 + portfolio_returns).cumprod()
    rolling_max = cumulative_returns.cummax()
    drawdown = cumulative_returns / rolling_max - 1

    drawdown_df = pd.DataFrame({
        "Date": portfolio_returns.index,
        "Drawdown": drawdown
    }).set_index("Date")

    st.line_chart(drawdown_df)

    # 2. ⚠️ Simulated Stress Test Scenarios
    st.markdown("---")
    st.subheader("⚠️ Simulated Stress Test Scenarios")

    stress_df = pd.DataFrame({
        "Scenario": ["Equity Crash", "Rate Shock", "FX Devaluation", "Liquidity Crunch"],
        "Portfolio Impact (%)": [-15.2, -8.5, -6.1, -11.3]
    })

    fig_stress = px.bar(
        stress_df, 
        x="Scenario", 
        y="Portfolio Impact (%)", 
        color="Portfolio Impact (%)",
        color_continuous_scale="RdBu",
        title="Portfolio Loss Under Stress Scenarios"
    )
    st.plotly_chart(fig_stress, use_container_width=True)

    # 3. 🎯 Risk Factor Exposure
    st.markdown("---")
    st.subheader("🎯 Exposure by Risk Factor")

    risk_factors_df = pd.DataFrame({
        "Factor": ["Interest Rate", "Credit", "Equity", "FX", "Liquidity"],
        "Exposure (%)": [35, 30, 20, 10, 5]
    })

    fig_factors = px.pie(
        risk_factors_df, 
        names="Factor", 
        values="Exposure (%)", 
        title="Risk Factor Attribution"
    )
    st.plotly_chart(fig_factors, use_container_width=True)


st.markdown("## Risk Trends")
with st.expander("📈 Risk Trends - Click to expand / collapse", expanded=False):
    # === Rolling Volatility and Drawdowns ===
    st.subheader("📉 Rolling Risk Trends")
    rolling_vol = portfolio_returns.rolling(30).std() * np.sqrt(252)
    rolling_max = (1 + portfolio_returns).cumprod().cummax()
    drawdowns = (1 + portfolio_returns).cumprod() / rolling_max - 1

    col4, col5 = st.columns(2)
    fig_vol = go.Figure()
    fig_vol.add_trace(go.Scatter(x=rolling_vol.index, y=rolling_vol, name="30D Volatility"))
    fig_vol.update_layout(xaxis_title="Date", yaxis_title="Volatility")
    col4.plotly_chart(fig_vol, use_container_width=True)

    # === Ticker Drilldown ===
    st.subheader("🔎 Explore Stock Price")
    selected = st.selectbox("Choose a ticker:", options=close_prices.columns)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=close_prices.index, y=close_prices[selected], name=selected))
    fig.update_layout(title=f"{selected} Price History", xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(fig, use_container_width=True)




