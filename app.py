import streamlit as st
import pandas as pd
import json
import os

# Define paths to the folders
income_statement_folder = 'IncomeStatementStockData'  # Update this path
stock_data_folder = 'StockData'                       # Update this path

# Helper function to find a matching file name in a folder based on a prefix match
def find_file_by_prefix(folder_path, stock_name, extension=None):
    for file_name in os.listdir(folder_path):
        if file_name.lower().startswith(stock_name.lower()):
            if extension is None or file_name.endswith(f".{extension}"):
                return os.path.join(folder_path, file_name)
    return None

# Function to load JSON income statement file
def load_income_statement(stock_name):
    json_path = find_file_by_prefix(income_statement_folder, stock_name, "json")
    if json_path:
        with open(json_path) as f:
            data = json.load(f)
        income_df = pd.DataFrame(data["IncomeStatement"])
        return income_df
    else:
        st.error(f"Income statement for '{stock_name}' not found. Available income statements: {', '.join(list_available_files(income_statement_folder, 'json'))}")
        return None

# Function to load Excel stock data file
def load_stock_data(stock_name):
    excel_path = find_file_by_prefix(stock_data_folder, stock_name, "xlsx")
    if excel_path:
        stock_df = pd.read_excel(excel_path)
        return stock_df
    else:
        st.error(f"Stock data for '{stock_name}' not found. Available stock data: {', '.join(list_available_files(stock_data_folder, 'xlsx'))}")
        return None

# Function to list available files in a folder with a specific extension
def list_available_files(folder_path, extension):
    return [file.split('.')[0] for file in os.listdir(folder_path) if file.endswith(f".{extension}")]

# Function to interpret command and fetch data
def fetch_data(command):
    command = command.lower().strip()
    
    # Check if the command is for income statement data
    if command.startswith("import income statement of"):
        parts = command.split()
        stock_name = parts[-1].upper()  # Last word is the stock name
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
st.write("Enter command to fetch data (e.g., 'import income statement of TCS' or 'import stock price of TCS').")

# Text input for command
command = st.text_input("Command")

# Button to execute command
if st.button("Fetch Data"):
    fetch_data(command)
