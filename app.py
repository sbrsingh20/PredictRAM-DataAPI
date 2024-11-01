import streamlit as st
import pandas as pd
import json
import os

# Define paths to the folders
income_statement_folder = '/to/IncomeStatementStockData'  # Update this path
stock_data_folder = '/to/StockData'                       # Update this path

# Function to load JSON income statement file
def load_income_statement(stock_name):
    try:
        json_path = os.path.join(income_statement_folder, f"{stock_name}.json")
        with open(json_path) as f:
            data = json.load(f)
        income_df = pd.DataFrame(data["IncomeStatement"])
        return income_df
    except FileNotFoundError:
        st.error(f"Income statement for '{stock_name}' not found.")
        return None

# Function to load Excel stock data file
def load_stock_data(stock_name):
    try:
        excel_path = os.path.join(stock_data_folder, f"{stock_name}.xlsx")
        stock_df = pd.read_excel(excel_path)
        return stock_df
    except FileNotFoundError:
        st.error(f"Stock data for '{stock_name}' not found.")
        return None

# Function to interpret command and fetch data
def fetch_data(command):
    command = command.lower().strip()
    parts = command.split()
    
    if len(parts) >= 3 and parts[0] == "import":
        stock_name = parts[1].upper()
        
        if "income statement" in command:
            st.write(f"Fetching Income Statement Data for {stock_name}")
            income_df = load_income_statement(stock_name)
            if income_df is not None:
                st.write(income_df)
        
        elif "stock price" in command:
            st.write(f"Fetching Stock Price Data for {stock_name}")
            stock_df = load_stock_data(stock_name)
            if stock_df is not None:
                st.write(stock_df)
        
        else:
            st.write("Invalid command. Use 'income statement' or 'stock price'.")
    else:
        st.write("Invalid command format. Use 'import [stock_name] income statement' or 'import stock price of [stock_name]'.")

# Streamlit App Layout
st.title("Stock Data Terminal")
st.write("Enter command to fetch data (e.g., 'import TCS income statement' or 'import stock price of TCS').")

# Text input for command
command = st.text_input("Command")

# Button to execute command
if st.button("Fetch Data"):
    fetch_data(command)
