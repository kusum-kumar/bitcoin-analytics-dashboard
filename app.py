
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Bitcoin Analytics Dashboard",
    page_icon="₿",
    layout="wide"
)
# Professional Dark Navy Theme
st.markdown("""
<style>
.stApp {
    background-color: #0B1120;
    color: #E5E7EB;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

h1, h2, h3 {
    color: #F8FAFC !important;
}

p, label {
    color: #CBD5E1;
}

[data-testid="stMetric"] {
    background-color: #1E293B;
    border: 1px solid #334155;
    padding: 20px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# Dashboard title
st.title("₿ Bitcoin Analytics Dashboard")

st.subheader("Financial Performance & Risk Analysis")

st.write(
    "Welcome to my interactive Bitcoin analytics dashboard."
)

# Sidebar
st.sidebar.title("Dashboard Settings")

uploaded_file = st.sidebar.file_uploader(
    "Upload Bitcoin CSV File",
    type=["csv"]
)

# Load data
if uploaded_file is not None:

    data = pd.read_csv(uploaded_file)

    st.success("Bitcoin data uploaded successfully!")

    st.subheader("Bitcoin Historical Data")
    
    # Prepare Bitcoin data
    data["Date"] = pd.to_datetime(data["Date"])
    data = data.sort_values("Date")

    # Calculate daily returns
    data["Daily_Return"] = data["Close"].pct_change()

    # Total return
    total_return = (
        data["Close"].iloc[-1] / data["Close"].iloc[0] - 1
    ) * 100

    # Annualized volatility
    volatility = data["Daily_Return"].std() * np.sqrt(365) * 100

    # Maximum drawdown
    cumulative_max = data["Close"].cummax()
    drawdown = data["Close"] / cumulative_max - 1
    max_drawdown = drawdown.min() * 100

    # Latest Bitcoin price
    latest_price = data["Close"].iloc[-1]

    # Display KPI cards
    st.subheader("Bitcoin Performance Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Latest Bitcoin Price", f"${latest_price:,.2f}")
    col2.metric("Total Return", f"{total_return:,.2f}%")
    col3.metric("Annualized Volatility", f"{volatility:,.2f}%")
    col4.metric("Maximum Drawdown", f"{max_drawdown:,.2f}%")

    # Bitcoin Historical Price Chart
    st.subheader("Bitcoin Price Performance")

    fig = px.line(
        data,
        x="Date",
        y="Close",
        title="Bitcoin Historical Closing Price",
        labels={
            "Date": "Date",
            "Close": "Bitcoin Price (USD)"
        }
    )

    fig.update_layout(
        template="plotly_white",
        height=500,
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)
        # Bitcoin Candlestick Chart
    st.subheader("Bitcoin Candlestick Analysis")

    candle_fig = go.Figure(data=[go.Candlestick(
        x=data["Date"],
        open=data["Open"],
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
        name="Bitcoin"
    )])

    candle_fig.update_layout(
        template="plotly_dark",
        height=550,
        xaxis_title="Date",
        yaxis_title="Bitcoin Price (USD)",
        xaxis_rangeslider_visible=False
    )

    st.plotly_chart(candle_fig, use_container_width=True)
        # Bitcoin Worst Crash Days
    st.subheader("Bitcoin - Worst Crash Days in History")

    worst_days = data.nsmallest(10, "Daily_Return").copy()
    worst_days["Daily_Return_Percent"] = worst_days["Daily_Return"] * 100

    crash_fig = px.bar(
        worst_days,
        x="Date",
        y="Daily_Return_Percent",
        title="Top 10 Worst Bitcoin Daily Returns",
        hover_data={"Daily_Return_Percent": ":.2f"}
    )

    crash_fig.update_layout(
        template="plotly_dark",
        height=450,
        xaxis_title="Date",
        yaxis_title="Daily Return (%)"
    )

    st.plotly_chart(crash_fig, use_container_width=True)
        # Bitcoin Yearly Returns
    st.subheader("Bitcoin Yearly Returns - Best vs Worst Years")

    yearly_data = data.copy()
    yearly_data["Year"] = yearly_data["Date"].dt.year

    yearly_returns = (
        yearly_data.groupby("Year")["Close"]
        .agg(["first", "last"])
    )

    yearly_returns["Return (%)"] = (
        (yearly_returns["last"] / yearly_returns["first"] - 1) * 100
    )

    yearly_fig = px.bar(
        yearly_returns.reset_index(),
        x="Year",
        y="Return (%)",
        title="Bitcoin Annual Returns",
        color="Return (%)",
        color_continuous_scale="RdYlGn"
    )

    yearly_fig.update_layout(
        template="plotly_dark",
        height=450,
        xaxis_title="Year",
        yaxis_title="Return (%)",
        showlegend=False
    )

    st.plotly_chart(yearly_fig, use_container_width=True)
    
    st.dataframe(data.head())

else:

    st.info("Please upload your Bitcoin CSV file.")
