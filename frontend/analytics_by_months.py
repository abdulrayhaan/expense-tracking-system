import streamlit as st
import requests
import pandas as pd

API_URL="http://127.0.0.1:8000"

def analytics_by_months_tab():
    st.title("Expense Breakdown by Months")
    response=requests.post(f"{API_URL}/monthly_summary/")
    response=response.json()
    data=response
    df=pd.DataFrame(data)
    df.rename(
        columns={
            "expense_month":"Month Number",
            "Month" : "Month Name"
        },inplace=True
    )
    df.set_index("Month Number",inplace=True)
    st.bar_chart(data=df.set_index('Month Name')['Total'],width=0, height=0, use_container_width=True)

    df["Total"] = df["Total"].map("{:.2f}".format)
    st.table(df)
