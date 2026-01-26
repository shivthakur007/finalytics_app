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

    
#Table View
if st.session_state.expenses:
    df = pd.DataFrame(
        st.session_state.expenses.items(),
        columns = ["Expense" , "Amount"]
    )
    st.dataframe(df, use_container_width = True)

#Delete section
    st.subheader("Delete Expense")
    expense_to_delete = st.selectbox("select an expense to delete",
                                     list(st.session_state.expenses.keys())
                                    )
    if st.button("Delete an Expense"):
        del st.session_state.expenses[expense_to_delete]
        st.success(f"Deleted {expense_to_delete}")
        
    
    #Optional Total
    st.info(f"Total Expense: ${df['Amount'].sum()}") 
else:
    st.warning("No Expense added Yet")
        
    

