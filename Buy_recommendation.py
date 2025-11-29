import streamlit as st
import math

st.set_page_config(page_title="20/4/10 Car Affordability Checker", layout="centered")

st.title("🚗 20/4/10 Car Affordability Checker")
st.write("Check if your car purchase follows the safe 20/4/10 financial rule.")

# --- EMI Calculation Function ---
def calculate_emi(principal, annual_interest_rate, years):
    monthly_rate = (annual_interest_rate / 100) / 12
    months = years * 12

    if monthly_rate == 0:
        return principal / months

    emi = principal * monthly_rate * (1 + monthly_rate) ** months / ((1 + monthly_rate) ** months - 1)
    return emi


# --- INPUTS ---
st.header("Input Your Details")

monthly_income = st.number_input("Monthly Income (₹):", min_value=0, step=1000)
monthly_expense = st.number_input("Monthly Car Expense Budget (fuel, insurance etc.) (Excl. EMI) (₹):", min_value=0, step=500)
car_price = st.number_input("Car Price (₹):", min_value=0, step=10000)
down_payment = st.number_input("Down Payment (₹):", min_value=0, step=10000)
loan_years = st.number_input("Loan Tenure (Years):", min_value=1.0, max_value=7.0, step=0.5)
interest_rate = st.number_input("Annual Interest Rate (%):", min_value=0.0, step=0.1)


if st.button("Check 20/4/10 Recommendation"):
    if monthly_income == 0 or car_price == 0:
        st.error("Please enter valid income and car price.")
    else:
        loan_amount = max(car_price - down_payment, 0)
        emi = calculate_emi(loan_amount, interest_rate, loan_years)
        total_monthly_cost = emi + monthly_expense

        st.subheader("📘 Loan Summary")
        st.write(f"**Loan Amount:** ₹{loan_amount:,.2f}")
        st.write(f"**Estimated EMI:** ₹{emi:,.2f}")
        st.write(f"**Total Monthly Car Cost:** ₹{total_monthly_cost:,.2f}")

        # RULE CHECKS
        rule_down = down_payment >= 0.20 * car_price
        rule_tenure = loan_years <= 4
        rule_cost = total_monthly_cost <= 0.10 * monthly_income

        st.subheader("📊 20/4/10 Rule Check")

        st.write(f"20% Down Payment: {'✅' if rule_down else '❌'}")
        st.write(f"Loan Tenure ≤ 4 Years: {'✅' if rule_tenure else '❌'}")
        st.write(f"Total Car Cost ≤ 10% of Income: {'✅' if rule_cost else '❌'}")

        if rule_down and rule_tenure and rule_cost:
            st.success("🎉 Recommended! This car follows the 20/4/10 rule.")
        else:
            st.error("⚠ Not Recommended based on the 20/4/10 rule.")
            if not rule_down:
                st.write(f"- You need at least **₹{0.20 * car_price:,.2f}** down payment.")
            if not rule_tenure:
                st.write("- Reduce loan tenure to **4 years or less**.")
            if not rule_cost:
                st.write(f"- Total monthly car cost should be ≤ **₹{0.10 * monthly_income:,.2f}**.")


st.markdown("---")
st.caption("Built with ❤️ using Streamlit")
