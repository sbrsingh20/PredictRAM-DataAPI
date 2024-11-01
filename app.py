import streamlit as st
import pandas as pd
import json
import os

# Define paths to the folders
income_statement_folder = 'IncomeStatementStockData'  # Update this path
stock_data_folder = 'StockData'                       # Update this path

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
    
    # Check if the command is for income statement data
    if command.startswith("import") and "income statement" in command:
        parts = command.split()
        stock_name = parts[1].upper()  # Second word is the stock name
        st.write(f"Fetching Income Statement Data for {stock_name}")
        income_df = load_income_statement(stock_name)
        if income_df is not None:
            st.write(income_df)
    
    # Check if the command is for stock price data
    elif command.startswith("import stock price of"):
        parts = command.split()
        stock_name = parts[-1].upper()  # Last word is the stock name
        st.write(f"Fetching Stock Price Data for {stock_name}")
        stock_df = load_stock_data(stock_name)
        if stock_df is not None:
            st.write(stock_df)
    
    # Handle invalid command format
    else:
        st.write("Invalid command format. Use 'import income statement of [stock_name]' or 'import stock price of [stock_name]'.")

# Streamlit App Layout
st.title("Stock Data Terminal")
st.write("Enter command to fetch data (e.g., 'import TCS income statement' or 'import stock price of TCS').")

# Text input for command
command = st.text_input("Command")

# Button to execute command
if st.button("Fetch Data"):
    fetch_data(command)
