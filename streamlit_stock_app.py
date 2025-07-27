import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(page_title="Stock Range Analyzer", layout="wide")
st.title("📊 Stock Range Analyzer App")

# --- Sidebar Inputs ---
with st.sidebar:
    ticker = st.text_input("Enter Stock Ticker (e.g., HEROMOTOCO.NS)", "HEROMOTOCO.NS")
    start_date = st.date_input("Start Date", pd.to_datetime("2022-04-01"))
    end_date = st.date_input("End Date", pd.to_datetime("2024-03-31"))
    fetch = st.button("📥 Fetch Stock Data")

# --- Main App ---
if fetch:
    if start_date >= end_date:
        st.error("End date must be after start date.")
    else:
        try:
            st.info(f"Fetching data for **{ticker}**...")
            data = yf.download(ticker, start=start_date, end=end_date)
            stock = yf.Ticker(ticker)
            info = stock.info

            if data.empty:
                st.warning("No data found. Please check the ticker or date range.")
            else:
                # --- Stock Info ---
                st.subheader("🏢 Stock Summary")
                st.markdown(f"**Company Name:** {info.get('longName', 'N/A')}")
                st.markdown(f"**Sector:** {info.get('sector', 'N/A')}")
                st.markdown(f"**Current Price:** ₹ {info.get('currentPrice', 'N/A')}")
                st.markdown(f"**Market Cap:** {info.get('marketCap', 'N/A'):,}")
                st.markdown(f"**PE Ratio:** {info.get('trailingPE', 'N/A')}")
                st.markdown(f"**Dividend Yield:** {info.get('dividendYield', 'N/A')}")
                st.markdown(f"**52 Week High:** ₹ {info.get('fiftyTwoWeekHigh', 'N/A')}")
                st.markdown(f"**52 Week Low:** ₹ {info.get('fiftyTwoWeekLow', 'N/A')}")

                # --- Calculations ---
                data['Range'] = data['High'] - data['Low']
                data['MA20'] = data['Close'].rolling(window=20).mean()
                data['MA50'] = data['Close'].rolling(window=50).mean()

                # --- Data Table ---
                st.subheader("📈 Sample Data with Range and Moving Averages")
                st.dataframe(data[['Open', 'High', 'Low', 'Close', 'Range', 'MA20', 'MA50']].dropna().tail(10))

                # --- Matplotlib Range Plot ---
                st.subheader("📊 Daily Range Plot")
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.plot(data.index, data['Range'], color='green', label='Daily Range')
                ax.set_title(f"Daily Range for {ticker}")
                ax.set_xlabel("Date")
                ax.set_ylabel("Range (High - Low)")
                ax.legend()
                ax.grid(True)
                st.pyplot(fig)

                # --- Plotly Candlestick Chart ---
                st.subheader("🕯️ Candlestick Chart with Moving Averages")
                fig2 = go.Figure()
                fig2.add_trace(go.Candlestick(
                    x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'],
                    name="Candlestick"
                ))
                fig2.add_trace(go.Scatter(
                    x=data.index, y=data['MA20'], line=dict(color='orange', width=1), name="MA 20"
                ))
                fig2.add_trace(go.Scatter(
                    x=data.index, y=data['MA50'], line=dict(color='blue', width=1), name="MA 50"
                ))
                fig2.update_layout(xaxis_title='Date', yaxis_title='Price (₹)', template='plotly_dark')
                st.plotly_chart(fig2, use_container_width=True)

                # --- Download CSV ---
                st.subheader("📥 Download Processed Data")
                csv = data.to_csv().encode('utf-8')
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"{ticker}_stock_data.csv",
                    mime='text/csv'
                )

        except Exception as e:
            st.error(f"❌ Error fetching data: {e}")



