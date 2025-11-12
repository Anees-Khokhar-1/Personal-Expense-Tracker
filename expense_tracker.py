import os
from datetime import datetime
from utils.file_handler import load_expenses, save_expenses
from utils.summary import summarize_by_category, total_expenses, filter_by_month, format_currency
from utils.chart import plot_expense_summary

DATA_FILE = os.path.join("data", "expenses.csv")
CATEGORIES = ["Food", "Transport", "Entertainment", "Bills", "Shopping", "Other"]

def prompt_date():
    s = input("Enter date (YYYY-MM-DD) [today]: ").strip()
    if not s:
        return str(datetime.today().date())
    # basic validation
    try:
        datetime.fromisoformat(s)
        return s
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD. Try again.")
        return prompt_date()

def prompt_category():
    print("Categories:", ", ".join(CATEGORIES))
    c = input("Enter category (or type new category): ").strip()
    return c if c else "Other"

def prompt_amount():
    s = input("Enter amount: ").strip()
    try:
        return float(s)
    except ValueError:
        print("Invalid amount. Try again.")
        return prompt_amount()

def add_expense(expenses):
    date = prompt_date()
    category = prompt_category()
    amount = prompt_amount()
    description = input("Enter description: ").strip()
    expenses.append({
        "Date": date,
        "Category": category,
        "Amount": float(amount),
        "Description": description
    })
    save_expenses(DATA_FILE, expenses)
    print("Expense added.")

def view_expenses(expenses):
    if not expenses:
        print("No expenses found.")
        return
    print(f"{'Index':<6} {'Date':<12} {'Category':<15} {'Amount':<12} {'Description'}")
    print("-" * 70)
    for i, e in enumerate(expenses, start=1):
        print(f"{i:<6} {e['Date']:<12} {e['Category']:<15} {format_currency(float(e['Amount'])):<12} {e['Description']}")

def edit_expense(expenses):
    view_expenses(expenses)
    if not expenses:
        return
    try:
        idx = int(input("Enter the index number to edit (0 to cancel): ").strip())
    except ValueError:
        print("Invalid input.")
        return
    if idx == 0:
        return
    if idx < 1 or idx > len(expenses):
        print("Index out of range.")
        return
    e = expenses[idx-1]
    print("Leave blank to keep current value.")
    new_date = input(f"Date [{e['Date']}]: ").strip() or e['Date']
    new_category = input(f"Category [{e['Category']}]: ").strip() or e['Category']
    new_amount_raw = input(f"Amount [{e['Amount']}]: ").strip()
    new_amount = float(new_amount_raw) if new_amount_raw else float(e['Amount'])
    new_description = input(f"Description [{e['Description']}]: ").strip() or e['Description']

    e['Date'] = new_date
    e['Category'] = new_category
    e['Amount'] = float(new_amount)
    e['Description'] = new_description

    save_expenses(DATA_FILE, expenses)
    print("Expense updated.")

def delete_expense(expenses):
    view_expenses(expenses)
    if not expenses:
        return
    try:
        idx = int(input("Enter the index number to delete (0 to cancel): ").strip())
    except ValueError:
        print("Invalid input.")
        return
    if idx == 0:
        return
    if idx < 1 or idx > len(expenses):
        print("Index out of range.")
        return
    confirm = input(f"Delete expense #{idx}? (y/n): ").strip().lower()
    if confirm == 'y':
        removed = expenses.pop(idx-1)
        save_expenses(DATA_FILE, expenses)
        print("Deleted:", removed)
    else:
        print("Canceled.")

def show_summary(expenses):
    if not expenses:
        print("No expenses.")
        return
    by_cat = summarize_by_category(expenses)
    print("\nSummary by category:")
    for k, v in by_cat.items():
        print(f"  {k}: {format_currency(v)}")
    print("Total:", format_currency(total_expenses(expenses)))

def show_monthly_summary(expenses):
    try:
        y = int(input("Enter year (e.g., 2025): ").strip())
        m = int(input("Enter month (1-12): ").strip())
    except ValueError:
        print("Invalid year/month.")
        return
    month_exp = filter_by_month(expenses, y, m)
    if not month_exp:
        print("No expenses for that month.")
        return
    print(f"\nExpenses for {y}-{m:02d}:")
    view_expenses(month_exp)
    print("\nSummary for month:")
    by_cat = summarize_by_category(month_exp)
    for k, v in by_cat.items():
        print(f"  {k}: {format_currency(v)}")
    print("Total:", format_currency(total_expenses(month_exp)))

def show_chart(expenses):
    # You might want to select full data or a month
    choice = input("Chart for (1) All time or (2) Specific month? [1/2]: ").strip()
    if choice == '2':
        try:
            y = int(input("Year (e.g., 2025): ").strip())
            m = int(input("Month (1-12): ").strip())
        except ValueError:
            print("Invalid year/month.")
            return
        data = filter_by_month(expenses, y, m)
    else:
        data = expenses
    plot_expense_summary(data)

def export_copy(expenses):
    from pathlib import Path
    p = input("Enter export filename (e.g., exports/my_backup.csv): ").strip()
    if not p:
        print("Cancelled.")
        return
    Path(os.path.dirname(p) or ".").mkdir(parents=True, exist_ok=True)
    save_expenses(p, expenses)
    print(f"Exported to {p}")

def main():
    os.makedirs("data", exist_ok=True)
    os.makedirs("charts", exist_ok=True)

    expenses = load_expenses(DATA_FILE)

    while True:
        print("\n--- Personal Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Edit Expense")
        print("4. Delete Expense")
        print("5. Show Summary (all time)")
        print("6. Show Monthly Summary")
        print("7. Show Chart")
        print("8. Export CSV copy")
        print("9. Exit")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            add_expense(expenses)
        elif choice == '2':
            view_expenses(expenses)
        elif choice == '3':
            edit_expense(expenses)
        elif choice == '4':
            delete_expense(expenses)
        elif choice == '5':
            show_summary(expenses)
        elif choice == '6':
            show_monthly_summary(expenses)
        elif choice == '7':
            show_chart(expenses)
        elif choice == '8':
            export_copy(expenses)
        elif choice == '9':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
