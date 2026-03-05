import streamlit as st

st.markdown(
    """
    <h1 style='text-align: right; color: orange;'>
    Calculator 💸
    </h1>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("Calculators 🏦")

calculator = st.sidebar.selectbox(
    "Choose Calculator",
    ["Financial", "Simple", "Scientific"]
)

def simple_interest(p, r, t):
    return (p * r * t) / 100

def present_value(fv, r , n):
    r = r/100
    return fv/(1+r)**n

def compound_value(pv, r, n):
    r = r/100
    return pv*(1+r)**n

def compound_interest(pv, r, n):
    fv = compound_value(pv, r, n)
    return fv - pv

if calculator == "Financial":

    st.title("Financial Calculator")

    select = st.selectbox(
        "What do you want to know?",
        ["Simple Interest", "Compound Interest", "Present Value", "Future Value"]
    )

    if select == "Simple Interest":

        p = st.number_input("Principal")
        r = st.number_input("Rate (%)")
        t = st.number_input("Time (years)")

        if st.button("Calculate"):
            result = simple_interest(p, r, t)
            st.success(f"Simple Interest = {result}")
            
    elif select == "Present Value":

        fv = st.number_input("Future Value")
        r = st.number_input("Rate (%)")
        n = st.number_input("Time (years)")

        if st.button("Calculate"):
            result = present_value(fv, r, n)
            st.success(f"Present Value = {result}")
            
    elif select == "Compound Interest":

        pv = st.number_input("Principal")
        r = st.number_input("Rate (%)")
        n = st.number_input("Time (years)")

        if st.button("Calculate"):
            result = compound_interest(pv, r, n)
            st.success(f"Compound Interest = {result}")
            
    elif select == "Future Value":

        pv = st.number_input("Present Value")
        r = st.number_input("Rate (%)")
        n = st.number_input("Time (years)")

        if st.button("Calculate"):
            result = compound_value(pv, r, n)
            st.success(f"Future Value = {result}")
