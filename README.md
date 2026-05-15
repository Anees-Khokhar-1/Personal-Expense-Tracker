# Personal Expense Tracker

A simple console-based Personal Expense Tracker built with Python. It stores expenses in CSV format, summarizes spending by category, checks monthly budgets, and can generate a pie chart with Matplotlib.

## Features

- Add, view, edit, and delete expenses
- Validate dates, months, and positive expense amounts
- Store data in `data/expenses.csv`
- View all-time and monthly summaries
- Filter expenses by category, month, or keyword
- Sort expenses by date, amount, or category
- Check monthly spending against category budgets
- Export a CSV backup
- Generate a category pie chart in `charts/expense_summary.png`

## Project Structure

```text
Personal Expense Tracker/
├── expense_tracker.py
├── requirements.txt
├── data/
│   └── expenses.csv
├── charts/
│   └── expense_summary.png
└── utils/
    ├── chart.py
    ├── file_handler.py
    └── summary.py
```

## Setup

1. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:

   Windows:

   ```bash
   venv\Scripts\activate
   ```

   macOS/Linux:

   ```bash
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Run

```bash
python expense_tracker.py
```

## Menu Options

```text
1. Add Expense
2. View Expenses
3. Edit Expense
4. Delete Expense
5. Show Summary (all time)
6. Show Monthly Summary
7. Filter/Search Expenses
8. Sort Expenses
9. Check Monthly Budgets
10. Show Chart
11. Export CSV copy
12. Exit
```

## Data Format

Expenses are saved as CSV rows with these columns:

```csv
Date,Category,Amount,Description
2026-05-15,Food,1200,Lunch
```

Dates should use `YYYY-MM-DD` format. Amounts must be greater than zero.

## Budget Settings

Monthly category budgets are currently set in `expense_tracker.py`:

```python
MONTHLY_BUDGETS = {
    "Food": 50000,
    "Transport": 30000,
    "Entertainment": 15000,
    "Bills": 80000,
    "Shopping": 40000,
    "Other": 20000,
}
```

Edit these values to match your own monthly budget.

## Notes

- Currency is displayed as `Rs.` by default.
- Chart output is saved in the lowercase `charts` folder.
- `data/expenses.csv` and generated charts are user data, so they are ignored by Git in `.gitignore`.
