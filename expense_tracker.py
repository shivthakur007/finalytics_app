import streamlit as st 

st.title("Expense Tracker💸")
st.markdown("Money saved is equal to money earned")

# Initialise dictionary in session state
if "expenses" not in st.session_state:
    st.session_state.expenses = {}

#Take the user input 
exp = st.text_input("Enter the expense: ")
amt = st.number_input("Enter the Amount: ", min_value = 0, step = 50)

if st.button("Add Expense"):
    if exp:
        st.session_state.expenses[exp] = amt
        st.success(f"Added {exp} : ${amt}")
    else:
        st.warning("Please enter the expense")
        

st.subheader("Your Expenses") 
st.write(st.session_state.expenses)
    
    
    

