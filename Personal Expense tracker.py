# Personal_Expense_Tracker_Enhanced.py

"""
# 🧾 Personal Expense Tracker

This script provides a complete personal expense tracker with the following features:
- Add / Edit / Delete expenses.
- List all expenses in a table view.
- Generate summaries by Category and Month.
- Create visualizations (Bar chart for category totals, Line chart for monthly trend).
- Uses persistent storage in `expenses.json` with sample data auto-generation.
"""

# ## 📚 Imports and Setup
import json
import os
from typing import List, Dict, Any, Optional
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

DATA_FILE = "expenses.json"

# ## 💾 Data Loading & Saving (JSON)

def load_expenses(filename: str = DATA_FILE) -> List[Dict[str, Any]]:
    """Loads expenses from a JSON file."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
    except Exception:
        # If file is corrupted or unreadable, return an empty list
        return []
    return []

def save_expenses(expenses: List[Dict[str, Any]], filename: str = DATA_FILE) -> None:
    """Saves expenses to a JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(expenses, f, indent=4, ensure_ascii=False)

def ensure_sample_data():
    """Creates sample data if the expenses file is empty or doesn't exist."""
    expenses = load_expenses()
    if not expenses:
        print("No expenses found. Creating sample data...")
        sample = [
            {"Date": "2025-10-01", "Category": "Food", "Amount": 200.0, "Description": "Breakfast"},
            {"Date": "2025-10-03", "Category": "Transport", "Amount": 120.0, "Description": "Bus ticket"},
            {"Date": "2025-10-05", "Category": "Shopping", "Amount": 500.0, "Description": "Groceries"},
            {"Date": "2025-09-28", "Category": "Bills", "Amount": 1500.0, "Description": "Electricity bill"}
        ]
        save_expenses(sample)
        return sample
    return expenses

# ## 🧰 DataFrame Helper

def load_as_dataframe() -> pd.DataFrame:
    """Loads expenses and returns them as a pandas DataFrame."""
    expenses = load_expenses()
    df = pd.DataFrame(expenses)
    if df.empty:
        return df
    # Ensure correct data types
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.to_period('M')
    if 'Amount' in df.columns:
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0.0)
    return df

# ## 🔧 Core functions (add, edit, delete, list, summary, visuals)

def add_expense(date: str, category: str, amount: float, description: str) -> None:
    """Adds a new expense."""
    expenses = load_expenses()
    new_expense = {"Date": date, "Category": category, "Amount": float(amount), "Description": description}
    expenses.append(new_expense)
    save_expenses(expenses)
    print("✅ Expense added successfully.")

def list_expenses() -> pd.DataFrame:
    """Returns a DataFrame of all expenses."""
    df = load_as_dataframe()
    if df.empty:
        print("No expenses to display.")
        return df
    # Add a RowID for easy editing/deleting
    df_display = df.reset_index().rename(columns={'index':'RowID'})
    return df_display

def find_expense_index_by_rowid(rowid: int) -> Optional[int]:
    """Finds the list index corresponding to a DataFrame RowID."""
    expenses = load_expenses()
    if 0 <= rowid < len(expenses):
        return rowid
    return None

def edit_expense(index: int, date: str, category: str, amount: float, description: str) -> bool:
    """Edits an existing expense by its index."""
    expenses = load_expenses()
    if 0 <= index < len(expenses):
        expenses[index] = {"Date": date, "Category": category, "Amount": float(amount), "Description": description}
        save_expenses(expenses)
        return True
    return False

def delete_expense(index: int) -> bool:
    """Deletes an expense by its index."""
    expenses = load_expenses()
    if 0 <= index < len(expenses):
        expenses.pop(index)
        save_expenses(expenses)
        return True
    return False

def view_summary() -> Dict[str, pd.DataFrame]:
    """Generates summaries of expenses by category and month."""
    df = load_as_dataframe()
    if df.empty:
        return {"by_category": pd.DataFrame(), "by_month": pd.DataFrame()}
    by_category = df.groupby('Category', as_index=False)['Amount'].sum().sort_values('Amount', ascending=False)
    by_month = df.groupby('Month', as_index=False)['Amount'].sum().sort_values('Month')
    return {"by_category": by_category, "by_month": by_month}

def show_visual_summary():
    """Displays visualizations of the expense data."""
    df = load_as_dataframe()
    if df.empty:
        print("No data to visualize.")
        return
    
    summary = view_summary()
    by_category = summary['by_category']
    by_month = summary['by_month']

    # --- Plot 1: Expenses by Category ---
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.bar(by_category['Category'], by_category['Amount'], color='skyblue')
    ax1.set_title('Total Expenses by Category')
    ax1.set_xlabel('Category')
    ax1.set_ylabel('Total Amount (₹)')
    plt.xticks(rotation=45, ha='right')
    fig1.tight_layout()

    # --- Plot 2: Monthly Expense Trend ---
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    # Convert Period objects to string for stable plotting
    ax2.plot(by_month['Month'].astype(str), by_month['Amount'], marker='o', linestyle='-')
    ax2.set_title('Monthly Expense Trend')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Total Amount (₹)')
    plt.xticks(rotation=45, ha='right')
    fig2.tight_layout()

    print("Displaying plots... Close the plot windows to continue.")
    plt.show()

# ## 🧭 Command-Line Interface (CLI)

def main():
    """Main function to run the command-line interface."""
    ensure_sample_data()

    while True:
        print("\n--- 💰 Personal Expense Tracker ---")
        print("1. Add Expense")
        print("2. List Expenses")
        print("3. Edit Expense")
        print("4. Delete Expense")
        print("5. Show Summary Tables")
        print("6. Show Visual Summary (Plots)")
        print("7. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            date = input(f"Enter date (YYYY-MM-DD) [default: {datetime.today().strftime('%Y-%m-%d')}]: ") or datetime.today().strftime('%Y-%m-%d')
            category = input("Enter category: ")
            amount = float(input("Enter amount: "))
            description = input("Enter description: ")
            add_expense(date, category, amount, description)

        elif choice == '2':
            print("\n--- All Expenses ---")
            print(list_expenses())

        elif choice == '3':
            row_id = int(input("Enter the RowID of the expense to edit: "))
            index = find_expense_index_by_rowid(row_id)
            if index is not None:
                date = input("Enter new date (YYYY-MM-DD): ")
                category = input("Enter new category: ")
                amount = float(input("Enter new amount: "))
                description = input("Enter new description: ")
                if edit_expense(index, date, category, amount, description):
                    print(f"✅ Expense at RowID {row_id} updated.")
                else:
                    print(f"❌ Failed to update expense at RowID {row_id}.")
            else:
                print("❌ Invalid RowID.")

        elif choice == '4':
            row_id = int(input("Enter the RowID of the expense to delete: "))
            index = find_expense_index_by_rowid(row_id)
            if index is not None:
                if delete_expense(index):
                    print(f"🗑️ Expense at RowID {row_id} deleted.")
                else:
                    print(f"❌ Failed to delete expense at RowID {row_id}.")
            else:
                print("❌ Invalid RowID.")
                
        elif choice == '5':
            summary = view_summary()
            print("\n--- Summary by Category ---")
            print(summary['by_category'])
            print("\n--- Summary by Month ---")
            print(summary['by_month'])

        elif choice == '6':
            show_visual_summary()

        elif choice == '7':
            print("Exiting. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
