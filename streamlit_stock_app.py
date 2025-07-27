
import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

st.title("📊 Stock Range Analyzer App")

# User input for ticker and date range
ticker = st.text_input("Enter Stock Ticker (e.g., HEROMOTOCO.NS):", "HEROMOTOCO.NS")
start_date = st.date_input("Start Date", pd.to_datetime("2022-04-01"))
end_date = st.date_input("End Date", pd.to_datetime("2024-03-31"))

if st.button("Fetch Data"):
    try:
        data = yf.download(ticker, start=start_date, end=end_date)

        if data.empty:
            st.warning("No data found. Please check the ticker or date range.")
        else:
            data['Range'] = data['High'] - data['Low']
            st.subheader("Sample Data")
            st.dataframe(data[['High', 'Low', 'Range']].head())

            # Plotting
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(data.index, data['Range'], color='green', label='Daily Range')
            ax.set_title(f"Daily Range for {ticker}")
            ax.set_xlabel("Date")
            ax.set_ylabel("Range (High - Low)")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
