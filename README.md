# 💰 Personal Expense Tracker

This repository contains a Python-based Personal Expense Tracker, designed to help you efficiently manage, analyze, and visualize your spending. The application runs interactively within a **Jupyter Notebook**, providing a user-friendly, **widget-based interface** for ease of use.

Expenses are saved to an `expenses.json` file, ensuring your data persists between sessions. The tracker also includes powerful visualization features using **Matplotlib** to give you clear insights into your financial habits.

## ✨ Features

* **Interactive Widget UI**: A user-friendly tabbed menu to add, list, edit, delete, and summarize expenses.
* **Full Expense Management**:
    * **Add**: Record new expenses with a date, category, amount, and description.
    * **List**: View all recorded expenses in a clean, tabular format.
    * **Edit**: Modify the details of any existing expense by its RowID.
    * **Delete**: Remove an expense from your records by its RowID.
* **Data Persistence**: Expenses are automatically saved to and loaded from an `expenses.json` file.
* **Data Summaries**:
    * View total spending grouped by **category**.
    * View total spending grouped by **month**.
* **Rich Visualizations**:
    * Generate a **bar chart** to see the distribution of expenses across different categories.
    * Plot a **line chart** to analyze monthly spending trends over time.

## 📊 Visualizations Demo

The notebook automatically generates several plots to help you understand your spending patterns:

| Spending by Category (Bar Chart)                 | Monthly Spending Trend (Line Chart)              |
| :-----------------------------------------------: | :-----------------------------------------------: |
|                                                   |                                                   |

*(Note: These are example placeholders. The plots will generate based on your input data.)*

## 🛠️ Technologies Used

* **Python**: Core programming language.
* **Jupyter Notebook**: For creating the interactive application.
* **Pandas**: Used for data manipulation and creating data frames for analysis.
* **Matplotlib**: For creating static charts and visualizations.
* **ipywidgets**: For building the interactive UI components within the notebook.
* **JSON**: For storing and retrieving expense data.

## 🚀 How to Run

1.  **Clone the Repository**
    ```bash
    git clone <your-repository-url>
    cd your-repository-name
    ```

2.  **Install Dependencies**
    Make sure you have Python installed. Then, install the required libraries:
    ```bash
    pip install pandas matplotlib ipywidgets
    ```

3.  **Enable Jupyter Widgets**
    You must enable the `ipywidgets` extension for it to display correctly.
    ```bash
    # For classic Jupyter Notebook
    jupyter nbextension enable --py widgetsnbextension

    # For JupyterLab
    jupyter labextension install @jupyter-widgets/jupyterlab-manager
    ```

4.  **Launch Jupyter Notebook**
    In your terminal, run:
    ```bash
    jupyter notebook
    ```

5.  **Run the Tracker**
    * Open the `Personal_Expense_Tracker_Enhanced.ipynb` notebook.
    * Run all the cells in sequence.
    * The final cell will display the interactive widget interface, allowing you to manage your expenses.
