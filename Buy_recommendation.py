import streamlit as st

st.title("Car Loan Recommendation App")

# User Inputs
Mon_Income = st.number_input("Monthly Income:", min_value=0, step=100)
Expense = st.number_input("Monthly Expense:", min_value=0, step=50)
Car_price = st.number_input("Car Price:", min_value=0, step=500)
loan_tenure = st.number_input("Loan Tenure (Years):", min_value=0, step=1)
downpayment = st.number_input("Down Payment:", min_value=0, step=500)

# Process Button
if st.button("Check Recommendation"):

    if downpayment > 0.2 * Car_price:
        st.error("❌ Not Recommended: Down payment should not exceed 20% of the car price.")

    elif loan_tenure > 4:
        st.error("❌ Not Recommended: Loan tenure should not exceed 4 years.")

    elif Expense > 0.1 * Mon_Income:
        st.error("❌ Not Recommended: Expense exceeds 10% of monthly income.")

    else:
        st.success("✅ Recommended! All conditions are within the recommended limits.")

