#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd

st.set_page_config(page_title="Depreciation Calculator", layout="wide")
st.title("📉 Depreciation Calculator")
st.markdown("Supports **Straight-Line** and **Declining Balance** methods.")

# Sidebar inputs
st.sidebar.header("Asset Information")
name = st.sidebar.text_input("Asset Name", value="Machine A")
cost = st.sidebar.number_input("Acquisition Cost", min_value=0.0, value=10000.0)
life = st.sidebar.number_input("Useful Life (Years)", min_value=1, value=5)
salvage = st.sidebar.number_input("Salvage Value", min_value=0.0, value=2000.0)
method = st.sidebar.selectbox("Depreciation Method", ["Straight Line", "Declining Balance"])
rate = st.sidebar.slider("Declining Balance Rate (%)", min_value=10, max_value=50, value=20)

# Calculate depreciation
def straight_line(cost, life, salvage):
    dep = (cost - salvage) / life
    data = []
    book = cost
    for year in range(1, life + 1):
        book -= dep
        if book < salvage:
            book = salvage
        data.append({"Year": year, "Depreciation": round(dep, 2), "Book Value": round(book, 2)})
    return pd.DataFrame(data)

def declining_balance(cost, life, rate, salvage):
    rate /= 100
    data = []
    book = cost
    for year in range(1, life + 1):
        dep = round(book * rate, 2)
        if book - dep < salvage:
            dep = book - salvage
        book -= dep
        data.append({"Year": year, "Depreciation": dep, "Book Value": round(book, 2)})
    return pd.DataFrame(data)

# Session state for tracking multiple assets
if "assets" not in st.session_state:
    st.session_state.assets = {}

if st.sidebar.button("➕ Add Asset"):
    if salvage >= cost:
        st.sidebar.error("Salvage must be less than cost.")
    else:
        if method == "Straight Line":
            df = straight_line(cost, life, salvage)
        else:
            df = declining_balance(cost, life, rate, salvage)
        st.session_state.assets[name] = {
            "Method": method,
            "Cost": cost,
            "Life": life,
            "Salvage": salvage,
            "Data": df
        }
        st.sidebar.success(f"Added asset '{name}'")

# Display assets
if st.session_state.assets:
    for asset_name, details in st.session_state.assets.items():
        st.subheader(f"📦 {asset_name}")
        st.write(f"**Method:** {details['Method']}  |  **Cost:** {details['Cost']}  |  **Salvage:** {details['Salvage']}  |  **Life:** {details['Life']} years")
        st.dataframe(details["Data"], use_container_width=True)

        with st.expander("📈 Show Chart"):
            st.line_chart(details["Data"].set_index("Year")[["Book Value"]])

        csv = details["Data"].to_csv(index=False).encode("utf-8")
        st.download_button(f"📥 Download {asset_name} CSV", data=csv, file_name=f"{asset_name}_depreciation.csv", mime="text/csv")

    if st.button("🗑️ Clear All Assets"):
        st.session_state.assets.clear()
        st.success("All assets cleared.")

else:
    st.info("Add an asset from the sidebar to see results.")



# In[ ]:




