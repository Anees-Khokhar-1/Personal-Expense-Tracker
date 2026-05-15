import os
import matplotlib.pyplot as plt

def plot_expense_summary(expenses, output_dir="charts"):
    """
    Save and show a pie chart of expenses by category.
    - expenses: list of dicts with 'Category' and 'Amount'
    """
    if not expenses:
        print("No expenses to visualize.")
        return None

    # Compute totals
    summary = {}
    for e in expenses:
        category = e.get('Category') or "Uncategorized"
        summary[category] = summary.get(category, 0) + float(e.get('Amount') or 0)

    summary = {category: amount for category, amount in summary.items() if amount > 0}
    if not summary:
        print("No positive expenses to visualize.")
        return None

    categories = list(summary.keys())
    amounts = list(summary.values())

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "expense_summary.png")

    plt.figure(figsize=(7, 7))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
    plt.title("Expense Breakdown by Category")
    plt.tight_layout()
    plt.savefig(path)
    plt.show()
    plt.close()

    print(f"Chart saved to: {path}")
    return path
