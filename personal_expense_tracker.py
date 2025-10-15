
"""
personal_expense_tracker.py

Personal Expense Tracker with visualization (matplotlib optional)
Fixed and cleaned version.

Features:
- Add, edit, delete expenses
- View category/daily/monthly/overall summaries
- Save/load from JSON (expenses.json)
- Optional matplotlib visualizations (if matplotlib is installed)
- Robust input validation and error handling
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any

# Try importing matplotlib; if not available, visual features will be disabled.
try:
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:
    HAVE_MPL = False

DATA_FILE = "expenses.json"

def load_expenses(filename: str = DATA_FILE) -> List[Dict[str, Any]]:
    """Load expenses from a JSON file. Returns an empty list on error or if file missing."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, list):
            return []
        cleaned = []
        for e in data:
            if not isinstance(e, dict):
                continue
            amount = e.get("amount")
            category = e.get("category")
            date = e.get("date")
            # Basic validation and normalization
            try:
                amount = float(amount)
            except Exception:
                continue
            if not isinstance(category, str) or not category.strip():
                continue
            try:
                # accept strings like '2023-01-02' only
                datetime.strptime(date, "%Y-%m-%d")
            except Exception:
                continue
            cleaned.append({"amount": amount, "category": category.strip(), "date": date})
        return cleaned
    except Exception:
        return []

def save_expenses(expenses: List[Dict[str, Any]], filename: str = DATA_FILE):
    """Save expenses to a JSON file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(expenses, f, indent=4, ensure_ascii=False)
    except Exception as exc:
        print(f"Error saving expenses: {exc}")

def prompt_float(prompt: str) -> float:
    """Prompt the user for a float value; raises ValueError if invalid."""
    raw = input(prompt).strip()
    if raw == "":
        raise ValueError("No input")
    return float(raw)

def add_expense(expenses: List[Dict[str, Any]]):
    """Add a new expense record."""
    try:
        amount = prompt_float("Enter amount (e.g. 45.75): ")
    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
        return

    category = input("Enter category (e.g. Food, Transport, Entertainment): ").strip()
    if not category:
        print("Category cannot be empty.")
        return

    use_today = input("Use today's date? (y/n): ").strip().lower()
    if use_today == 'y' or use_today == '':
        date = datetime.today().strftime("%Y-%m-%d")
    else:
        date_str = input("Enter date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            date = date_str
        except Exception:
            print("Invalid date format. Use YYYY-MM-DD.")
            return

    record = {"amount": round(float(amount), 2), "category": category, "date": date}
    expenses.append(record)
    save_expenses(expenses)
    print("Expense added successfully.\n")

def view_summary(expenses: List[Dict[str, Any]]):
    """Display summary options for the user."""
    if not expenses:
        print("No expense records found.\n")
        return

    print("\n--- View Summary ---")
    print("1. Total spending by category")
    print("2. Total overall spending")
    print("3. Spending by date (daily summary)")
    print("4. Monthly summary")
    if HAVE_MPL:
        print("5. Show visual summary (pie/bar chart)")
    choice = input("Choose an option (1-{}): ".format(5 if HAVE_MPL else 4)).strip()

    if choice == "1":
        category = input("Enter category: ").strip()
        total = sum(e["amount"] for e in expenses if e["category"].lower() == category.lower())
        print(f"Total spent on '{category}': ${total:.2f}\n")

    elif choice == "2":
        total = sum(e["amount"] for e in expenses)
        print(f"Total spending overall: ${total:.2f}\n")

    elif choice == "3":
        daily = {}
        for e in expenses:
            daily[e["date"]] = daily.get(e["date"], 0) + e["amount"]
        print("\nDaily Spending Summary:")
        for date in sorted(daily.keys()):
            print(f"{date}: ${daily[date]:.2f}")
        print()

    elif choice == "4":
        monthly = {}
        for e in expenses:
            month = e["date"][:7]  # YYYY-MM
            monthly[month] = monthly.get(month, 0) + e["amount"]
        print("\nMonthly Spending Summary:")
        for month in sorted(monthly.keys()):
            print(f"{month}: ${monthly[month]:.2f}")
        print()

    elif choice == "5" and HAVE_MPL:
        show_visual_summary(expenses)

    else:
        print("Invalid choice.\n")

def show_visual_summary(expenses: List[Dict[str, Any]]):
    """Show pie or bar chart summaries using matplotlib (if available)."""
    if not HAVE_MPL:
        print("Matplotlib not available. Install it with `pip install matplotlib` to use visuals.")
        return

    if not expenses:
        print("No expenses to visualize.\n")
        return

    print("\n--- Visualization Menu ---")
    print("1. Pie chart (spending by category)")
    print("2. Bar chart (monthly spending)")
    choice = input("Choose a visualization (1-2): ").strip()

    if choice == "1":
        categories = {}
        for e in expenses:
            categories[e["category"]] = categories.get(e["category"], 0) + e["amount"]
        labels = list(categories.keys())
        sizes = list(categories.values())
        if not sizes:
            print("Nothing to plot.")
            return
        plt.figure(figsize=(7,7))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title("Spending by Category")
        plt.axis('equal')
        plt.show()

    elif choice == "2":
        monthly = {}
        for e in expenses:
            month = e["date"][:7]
            monthly[month] = monthly.get(month, 0) + e["amount"]
        months = sorted(monthly.keys())
        totals = [monthly[m] for m in months]
        if not totals:
            print("Nothing to plot.")
            return
        plt.figure(figsize=(8,5))
        plt.bar(months, totals)
        plt.xlabel("Month")
        plt.ylabel("Total Spending ($)")
        plt.title("Monthly Spending Trend")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("Invalid choice.")

def list_expenses(expenses: List[Dict[str, Any]]):
    """Print a numbered list of expenses."""
    if not expenses:
        print("No expenses found.")
        return
    print("\nExpenses:")
    for i, e in enumerate(expenses, 1):
        print(f"{i}. {e['date']} | {e['category']} | ${e['amount']:.2f}")
    print()

def delete_expense(expenses: List[Dict[str, Any]]):
    """Delete an expense by index."""
    if not expenses:
        print("No expenses to delete.\n")
        return
    list_expenses(expenses)
    try:
        idx = int(input("Enter the number of the expense to delete (0 to cancel): ").strip())
    except Exception:
        print("Invalid input.")
        return
    if idx == 0:
        print("Delete cancelled.\n")
        return
    if 1 <= idx <= len(expenses):
        removed = expenses.pop(idx-1)
        save_expenses(expenses)
        print(f"Removed: {removed['date']} | {removed['category']} | ${removed['amount']:.2f}\n")
    else:
        print("Index out of range.\n")

def edit_expense(expenses: List[Dict[str, Any]]):
    """Edit fields of an existing expense."""
    if not expenses:
        print("No expenses to edit.\n")
        return
    list_expenses(expenses)
    try:
        idx = int(input("Enter the number of the expense to edit (0 to cancel): ").strip())
    except Exception:
        print("Invalid input.")
        return
    if idx == 0:
        print("Edit cancelled.\n")
        return
    if not (1 <= idx <= len(expenses)):
        print("Index out of range.\n")
        return
    exp = expenses[idx-1]
    print(f"Editing {idx}. {exp['date']} | {exp['category']} | ${exp['amount']:.2f}")
    # Amount
    new_amount = input(f"New amount (press Enter to keep {exp['amount']}): ").strip()
    if new_amount:
        try:
            exp['amount'] = round(float(new_amount), 2)
        except Exception:
            print("Invalid amount input. Keeping old value.")
    # Category
    new_cat = input(f"New category (press Enter to keep '{exp['category']}'): ").strip()
    if new_cat:
        exp['category'] = new_cat
    # Date
    new_date = input(f"New date YYYY-MM-DD (press Enter to keep {exp['date']}): ").strip()
    if new_date:
        try:
            datetime.strptime(new_date, "%Y-%m-%d")
            exp['date'] = new_date
        except Exception:
            print("Invalid date. Keeping old date.")
    save_expenses(expenses)
    print("Expense updated.\n")

def main():
    print("=== Personal Expense Tracker ===")
    if not HAVE_MPL:
        print("Note: matplotlib not found. Visualizations are disabled.")
    expenses = load_expenses()
    while True:
        print("\nMenu:")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. Edit Expense")
        print("4. Delete Expense")
        print("5. List Expenses")
        print("6. Exit")
        choice = input("Choose an option (1-6): ").strip()
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_summary(expenses)
        elif choice == "3":
            edit_expense(expenses)
        elif choice == "4":
            delete_expense(expenses)
        elif choice == "5":
            list_expenses(expenses)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
