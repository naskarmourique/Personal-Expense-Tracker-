# 💰 Personal Expense Tracker

This repository contains a Python-based Personal Expense Tracker, designed to help you efficiently manage, analyze, and visualize your spending. The application runs interactively within a Jupyter Notebook, providing a command-line interface for ease of use.

Expenses are saved to an `expenses.json` file, ensuring your data persists between sessions. The tracker also includes powerful visualization features using **Matplotlib** and **Seaborn** to give you clear insights into your financial habits.

## ✨ Features

* **Interactive Menu**: A user-friendly menu to add, view, and list expenses. 
* **Expense Management**:
    * **Add**: Record new expenses with amount, category, and date. 
    * **List**: View all recorded expenses in a clean, chronological format. 
* **Data Persistence**: Expenses are automatically saved to and loaded from an `expenses.json` file. 
* **Data Summaries**:
    * Get total spending by a specific **category**. 
    * Calculate the **overall total** expense. 
    * View summaries grouped by **day** or **month**. 
* **Rich Visualizations**:
    * Generate a **pie chart** to see the distribution of expenses across different categories. 
    * Create a **bar chart** to compare total spending across different months. 
    * Plot a **line chart** to analyze monthly spending trends over time.

## 📊 Visualizations Demo

The notebook automatically generates several plots to help you understand your spending patterns:

| Spending by Category (Pie Chart)                | Monthly Spending (Bar Chart)                   |
| :----------------------------------------------: | :--------------------------------------------: |
|  |  |

*(Note: These are example images. The plots will generate based on your input data.)*

## 🛠️ Technologies Used

* **Python**: Core programming language.
* **Pandas**: Used for data manipulation and creating data frames for analysis.
* **Matplotlib & Seaborn**: For creating static charts and visualizations.
* **JSON**: For storing and retrieving expense data.

## 🚀 How to Run

1.  **Clone the Repository**
    ```bash
    git clone <your-repository-url>
    cd Personal_Expense_Tracker_Enhanced
    ```

2.  **Install Dependencies**
    Make sure you have Python installed. Then, install the required libraries:
    ```bash
    pip install pandas matplotlib seaborn
    ```

3.  **Launch Jupyter Notebook**
    In your terminal, run:
    ```bash
    jupyter notebook
    ```

4.  **Run the Tracker**
    * Open the `Personal_Expense_Tracker_Enhanced.ipynb` notebook.
    * Run the cells in sequence.
    * The final cell will start the interactive menu, allowing you to add and view your expenses. 


