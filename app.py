import streamlit as st
import pandas as pd
import json

# Load JSON file with Income Statement Data
json_path = '/mnt/data/WSTCSTPAPR.json'  # Update path as necessary
with open(json_path) as f:
    income_statement_data = json.load(f)

# Load Excel file with Stock Data
excel_path = '/mnt/data/ZEEMEDIA.NS_data.xlsx'  # Update path as necessary
stock_data = pd.read_excel(excel_path)

# Function to display data based on command
def display_data(command):
    command = command.lower()
    if "income statement" in command:
        st.write("Displaying Income Statement Data:")
        income_df = pd.DataFrame(income_statement_data["IncomeStatement"])
        st.write(income_df)
    elif "stock price" in command:
        st.write("Displaying Stock Price Data:")
        st.write(stock_data)
    else:
        st.write("Invalid command. Please try again.")

# Streamlit App Layout
st.title("Stock Data Terminal")
st.write("Enter command to fetch data (e.g., `import TCS income statement` or `import stock price of TCS`).")

# Text input for command
command = st.text_input("Command")

# Button to execute command
if st.button("Fetch Data"):
    display_data(command)
