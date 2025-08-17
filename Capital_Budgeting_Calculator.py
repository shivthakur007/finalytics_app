import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy_financial as npf

st.title("💰 Capital Budgeting Calculator")

# --- User Inputs ---
st.sidebar.header("Project Inputs")

initial_investment = st.sidebar.number_input("Initial Investment", min_value=0.0, value=100000.0, step=1000.0)
years = st.sidebar.number_input("Number of Years", min_value=1, value=5, step=1)
discount_rate = st.sidebar.number_input("Discount Rate (%)", min_value=0.0, value=10.0, step=0.5) / 100

# Enter cash flows for each year
st.subheader("Enter Cash Flows")
cash_flows = []
for i in range(1, years+1):
    cash = st.number_input(f"Year {i} Cash Flow", value=20000.0, step=1000.0)
    cash_flows.append(cash)

cash_flows = np.array(cash_flows)

# --- NPV Calculation ---
npv = -initial_investment
for t in range(years):
    npv += cash_flows[t] / ((1 + discount_rate) ** (t+1))

# --- IRR Calculation ---
irr = npf.irr([-initial_investment] + cash_flows.tolist())

# --- Payback Period ---
cumulative_cash = np.cumsum(cash_flows)
payback_period = None
for i, total in enumerate(cumulative_cash, start=1):
    if total >= initial_investment:
        payback_period = i
        break

# --- Profitability Index ---
present_values = [cf / ((1 + discount_rate) ** (t+1)) for t, cf in enumerate(cash_flows)]
pi = sum(present_values) / initial_investment

# --- Display Results ---
st.header("Results 📊")
st.write(f"**Net Present Value (NPV):** {npv:,.2f}")
st.write(f"**Internal Rate of Return (IRR):** {irr*100:.2f}%")
st.write(f"**Payback Period:** {payback_period} years" if payback_period else "Payback Period: Not achieved")
st.write(f"**Profitability Index (PI):** {pi:.2f}")

# --- Cash Flow Chart ---
st.subheader("Cash Flow Timeline")
years_list = [f"Year {i}" for i in range(1, years+1)]
df = pd.DataFrame({"Year": years_list, "Cash Flow": cash_flows})

st.bar_chart(df.set_index("Year"))

# --- NPV Sensitivity Curve ---
st.subheader("NPV vs Discount Rate")
rates = np.linspace(0, 0.3, 50)  # 0% to 30%
npvs = []
for r in rates:
    val = -initial_investment + sum(cash_flows[t] / ((1+r)**(t+1)) for t in range(years))
    npvs.append(val)

fig, ax = plt.subplots()
ax.plot(rates*100, npvs, marker="o")
ax.axhline(0, color="red", linestyle="--")
ax.set_xlabel("Discount Rate (%)")
ax.set_ylabel("NPV")
ax.set_title("NPV Sensitivity to Discount Rate")
st.pyplot(fig)
