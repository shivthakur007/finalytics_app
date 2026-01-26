import streamlit as st
import pandas as pd
import sqlite3

# ----------------------------
# Database Setup
# ----------------------------
conn = sqlite3.connect("expenses.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense TEXT NOT NULL,
    amount INTEGER NOT NULL
)
""")
conn.commit()

# ----------------------------
# Streamlit UI
# ----------------------------
st.title("Expense Tracker 💸")
st.markdown("Money saved is equal to money earned")

# ----------------------------
# Add Expense Section
# ----------------------------
st.subheader("Add Expense")

expense = st.text_input("Enter Expense Name")
amount = st.number_input("Enter Amount", min_value=0, step=50)

if st.button("Add Expense"):
    if expense.strip():
        cursor.execute(
            "INSERT INTO expenses (expense, amount) VALUES (?, ?)",
            (expense, amount)
        )
        conn.commit()
        st.success(f"Added {expense} : ₹{amount}")
    else:
        st.warning("Please enter an expense name")

# ----------------------------
# View Expenses
# ----------------------------
st.subheader("Your Expenses")

df = pd.read_sql("SELECT * FROM expenses", conn)

if not df.empty:
    st.dataframe(
        df.drop(columns=["id"]),
        use_container_width=True
    )

    # ----------------------------
    # Delete Expense
    # ----------------------------
    st.subheader("Delete Expense")

    expense_to_delete = st.selectbox(
        "Select an expense to delete",
        df["expense"].tolist()
    )

    if st.button("Delete Expense"):
        cursor.execute(
            "DELETE FROM expenses WHERE expense = ?",
            (expense_to_delete,)
        )
        conn.commit()
        st.success(f"Deleted {expense_to_delete}")

    # ----------------------------
    # Total Expense
    # ----------------------------
    total = df["amount"].sum()
    st.info(f"Total Expense: ₹{total}")

else:
    st.warning("No expenses added yet")

# ----------------------------
# Close connection safely
# ----------------------------
conn.close()
