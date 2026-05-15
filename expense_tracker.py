import os
from datetime import datetime
from pathlib import Path

from utils.chart import plot_expense_summary
from utils.file_handler import load_expenses, save_expenses
from utils.summary import (
    filter_by_category,
    filter_by_month,
    format_currency,
    search_expenses,
    sort_expenses,
    summarize_by_category,
    total_expenses,
)

DATA_FILE = os.path.join("data", "expenses.csv")
CHARTS_DIR = "charts"
CATEGORIES = ["Food", "Transport", "Entertainment", "Bills", "Shopping", "Other"]
MONTHLY_BUDGETS = {
    "Food": 50000,
    "Transport": 30000,
    "Entertainment": 15000,
    "Bills": 80000,
    "Shopping": 40000,
    "Other": 20000,
}


def prompt_date(default=None):
    label = f" [{default}]" if default else " [today]"
    while True:
        value = input(f"Enter date (YYYY-MM-DD){label}: ").strip()
        if not value:
            value = default or str(datetime.today().date())

        try:
            return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")


def prompt_category(default="Other"):
    print("Categories:", ", ".join(CATEGORIES))
    value = input(f"Enter category (or type new category) [{default}]: ").strip()
    return value or default


def prompt_amount(default=None):
    label = f" [{default}]" if default is not None else ""
    while True:
        value = input(f"Enter amount{label}: ").strip()
        if not value and default is not None:
            return float(default)

        try:
            amount = float(value)
        except ValueError:
            print("Invalid amount. Enter a number.")
            continue

        if amount <= 0:
            print("Amount must be greater than zero.")
            continue

        return amount


def prompt_year_month():
    while True:
        try:
            year = int(input("Enter year (e.g., 2026): ").strip())
            month = int(input("Enter month (1-12): ").strip())
        except ValueError:
            print("Invalid year/month. Enter numbers only.")
            continue

        if 1 <= month <= 12:
            return year, month

        print("Month must be between 1 and 12.")


def choose_expense_index(expenses, action):
    view_expenses(expenses)
    if not expenses:
        return None

    while True:
        value = input(f"Enter the index number to {action} (0 to cancel): ").strip()
        try:
            index = int(value)
        except ValueError:
            print("Invalid input. Enter a number.")
            continue

        if index == 0:
            return None
        if 1 <= index <= len(expenses):
            return index - 1

        print("Index out of range.")


def add_expense(expenses):
    date = prompt_date()
    category = prompt_category()
    amount = prompt_amount()
    description = input("Enter description: ").strip()
    expenses.append({
        "Date": date,
        "Category": category,
        "Amount": amount,
        "Description": description,
    })
    save_expenses(DATA_FILE, expenses)
    print("Expense added.")


def view_expenses(expenses):
    if not expenses:
        print("No expenses found.")
        return

    print(f"{'Index':<6} {'Date':<12} {'Category':<15} {'Amount':<16} {'Description'}")
    print("-" * 76)
    for index, expense in enumerate(expenses, start=1):
        print(
            f"{index:<6} "
            f"{expense.get('Date', ''):<12} "
            f"{expense.get('Category', ''):<15} "
            f"{format_currency(float(expense.get('Amount') or 0)):<16} "
            f"{expense.get('Description', '')}"
        )


def edit_expense(expenses):
    index = choose_expense_index(expenses, "edit")
    if index is None:
        return

    expense = expenses[index]
    print("Leave blank to keep current value.")

    expense["Date"] = prompt_date(expense["Date"])
    expense["Category"] = prompt_category(expense["Category"])
    expense["Amount"] = prompt_amount(expense["Amount"])
    description = input(f"Description [{expense['Description']}]: ").strip()
    if description:
        expense["Description"] = description

    save_expenses(DATA_FILE, expenses)
    print("Expense updated.")


def delete_expense(expenses):
    index = choose_expense_index(expenses, "delete")
    if index is None:
        return

    confirm = input(f"Delete expense #{index + 1}? (y/n): ").strip().lower()
    if confirm == "y":
        removed = expenses.pop(index)
        save_expenses(DATA_FILE, expenses)
        print("Deleted:", removed)
    else:
        print("Canceled.")


def show_summary(expenses):
    if not expenses:
        print("No expenses.")
        return

    by_category = summarize_by_category(expenses)
    print("\nSummary by category:")
    for category, amount in by_category.items():
        print(f"  {category}: {format_currency(amount)}")
    print("Total:", format_currency(total_expenses(expenses)))


def show_monthly_summary(expenses):
    year, month = prompt_year_month()
    month_expenses = filter_by_month(expenses, year, month)
    if not month_expenses:
        print("No expenses for that month.")
        return

    print(f"\nExpenses for {year}-{month:02d}:")
    view_expenses(month_expenses)
    show_summary(month_expenses)


def filter_and_search(expenses):
    print("\nFilter options")
    print("1. By category")
    print("2. By month")
    print("3. By keyword")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        category = prompt_category()
        results = filter_by_category(expenses, category)
    elif choice == "2":
        year, month = prompt_year_month()
        results = filter_by_month(expenses, year, month)
    elif choice == "3":
        keyword = input("Enter keyword: ").strip()
        results = search_expenses(expenses, keyword) if keyword else []
    else:
        print("Invalid choice.")
        return

    view_expenses(results)
    if results:
        print("Filtered total:", format_currency(total_expenses(results)))


def sort_and_view(expenses):
    print("\nSort options")
    print("1. Newest first")
    print("2. Oldest first")
    print("3. Highest amount")
    print("4. Lowest amount")
    print("5. Category")
    choice = input("Choose an option: ").strip()
    sort_map = {
        "1": "date_desc",
        "2": "date_asc",
        "3": "amount_desc",
        "4": "amount_asc",
        "5": "category",
    }

    sort_key = sort_map.get(choice)
    if not sort_key:
        print("Invalid choice.")
        return

    view_expenses(sort_expenses(expenses, sort_key))


def check_monthly_budgets(expenses):
    year, month = prompt_year_month()
    month_expenses = filter_by_month(expenses, year, month)
    if not month_expenses:
        print("No expenses for that month.")
        return

    by_category = summarize_by_category(month_expenses)
    print(f"\nBudget check for {year}-{month:02d}:")
    for category in sorted(set(MONTHLY_BUDGETS) | set(by_category)):
        spent = by_category.get(category, 0)
        budget = MONTHLY_BUDGETS.get(category)
        if budget is None:
            print(f"  {category}: {format_currency(spent)} spent (no budget set)")
            continue

        remaining = budget - spent
        status = "over budget" if remaining < 0 else "remaining"
        print(
            f"  {category}: {format_currency(spent)} spent / "
            f"{format_currency(budget)} budget, {format_currency(abs(remaining))} {status}"
        )


def show_chart(expenses):
    choice = input("Chart for (1) All time or (2) Specific month? [1/2]: ").strip()
    if choice == "2":
        year, month = prompt_year_month()
        data = filter_by_month(expenses, year, month)
    else:
        data = expenses

    plot_expense_summary(data, CHARTS_DIR)


def export_copy(expenses):
    path = input("Enter export filename (e.g., exports/my_backup.csv): ").strip()
    if not path:
        print("Cancelled.")
        return

    export_path = Path(path)
    if export_path.exists():
        confirm = input(f"{path} already exists. Overwrite? (y/n): ").strip().lower()
        if confirm != "y":
            print("Export cancelled.")
            return

    save_expenses(str(export_path), expenses)
    print(f"Exported to {export_path}")


def main():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    os.makedirs(CHARTS_DIR, exist_ok=True)

    expenses = load_expenses(DATA_FILE)

    while True:
        print("\n--- Personal Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Edit Expense")
        print("4. Delete Expense")
        print("5. Show Summary (all time)")
        print("6. Show Monthly Summary")
        print("7. Filter/Search Expenses")
        print("8. Sort Expenses")
        print("9. Check Monthly Budgets")
        print("10. Show Chart")
        print("11. Export CSV copy")
        print("12. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            edit_expense(expenses)
        elif choice == "4":
            delete_expense(expenses)
        elif choice == "5":
            show_summary(expenses)
        elif choice == "6":
            show_monthly_summary(expenses)
        elif choice == "7":
            filter_and_search(expenses)
        elif choice == "8":
            sort_and_view(expenses)
        elif choice == "9":
            check_monthly_budgets(expenses)
        elif choice == "10":
            show_chart(expenses)
        elif choice == "11":
            export_copy(expenses)
        elif choice == "12":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
