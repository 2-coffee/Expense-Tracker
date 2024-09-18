import calendar
import datetime
from dateutil.relativedelta import relativedelta


import streamlit as st
import plotly.graph_objects as go

#----- [SETTINGS] ------
# ```$ streamlit run app.py```
incomes = ["Salary","Blog","Other Income"]
expenses = ["Rent","Utilities","Groceries","Car","Other Expenses","Saving"]
currency = "USD"
page_title = "Income and Expense Tracker"
page_icon = "💸"
layout = "centered"
#-----------------------

st.set_page_config(page_title= page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

# --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---
years = [datetime.date.today().year , datetime.date.today().year + 1]
months = list(calendar.month_name[1:])

# --- iNPUT AND SAVE PERIODS ---
st.header(f"Data Entry in {currency}")
with st.form("entry_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    col1.selectbox("Select Month:", months, key = "month")
    col2.selectbox("Select Year:", years, key= "year")
    
    "---"
    with st.expander("Income"):
        for income in incomes:
            st.number_input(f"{income}", min_value=0, format="%i", step=10, key=income )
    with st.expander("Expenses"):
        for expense in expenses:
            st.number_input(f"{expense}", min_value=0,  format="%i", step=10, key=expense)
    with st.expander("Comment"):
        comment = st.text_area("",placeholder="Enter a comment here...")
    "---"
    submitted = st.form_submit_button("Save Data")
    if submitted: #remember the keys from earlier
        period = str(st.session_state["year"]) + "_" + str(st.session_state["month"])
        incomes = {income: st.session_state[income] for income in incomes}
        expenses = {expense: st.session_state[expense] for expense in expenses}

        # TODO: Insert values into our database
        st.write(f"incomes: {incomes}")
        st.write(f"expenses: {expenses}")
        st.success("Data Saved!")

# --- PLOT PERIODS ---
st.header("Data Visualization")
with st.form("SAved_periods"):
    #TODO: Get periods from database
    period = st.selectbox("Select Period:", ["2024_Januray"]) # need to get all of them later
    submitted = st.form_submit_button("Load")
    if submitted:
        # TODO: get data from database
        comment = "Some comment"
        incomes = {"Salary": 1500, "Blog":50,"Other":10}
        expenses = {'Rent': 34, 'Utilities': 4141, 'Groceries': 100, 'Car': 543, 'Other Expenses': 3, 'Saving': 23}


        total_income = sum(incomes.values())
        total_expense = sum(expenses.values())

        remaining_budget = total_income - total_expense
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Income",f"{total_income} {currency}")
        col2.metric("Total Expense",f"{total_expense} {currency}")
        col3.metric("Remaing Budget", f"{remaining_budget} {currency}")
        st.text(f"Comment: {comment}") 

        # Create sankey chart
        label = list(incomes.keys()) + ["Total Income"] + list(expenses.keys())
        print(label)
        source = [i for i in range(len(incomes))] + [len(incomes)]*len(expenses)
        target = [len(incomes)]*len(incomes) + [i for i in range(len(incomes)+1,len(label))]
        value = list(incomes.values()) + list(expenses.values())
        print(value)
        # Data to dict, dict to sankey
        link = dict(source=source, target = target, value = value)
        node = dict(label=label, pad=20, thickness=30, color ="#E694FF") #"#a1ff79"
        data = go.Sankey(link=link, node=node)

        # Plot it
        fig = go.Figure(data)
        fig.update_layout(margin=dict(l=0,r=0,t=5,b=5))
        st.plotly_chart(fig, use_container_width=True)