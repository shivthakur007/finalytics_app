import streamlit as st 
import pandas as pd

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
    
#Table View
if st.session_state.expenses:
    df = pd.DateFrame(
        st.session_state.expenses.items(),
        columns = ["Amount" , "Expense"]
    )
    st.dataframe(df, use_container_width = True)
    
    #Optional Total
    st.info(f"Total Expense: ${df['Amount'].sum()}") 
else:
    st.warning("No Expense added Yet")
        
    

