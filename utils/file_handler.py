import csv
import os

FIELDNAMES = ['Date', 'Category', 'Amount', 'Description']

def load_expenses(file_path):
    """
    Load expenses from a CSV file.
    Returns a list of dictionaries, each representing one expense.
    """
    expenses = []

    # Check if file exists; if not, return empty list
    if not os.path.exists(file_path):
        return expenses

    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not row:
                    continue

                cleaned_row = {field: (row.get(field) or "").strip() for field in FIELDNAMES}

                try:
                    cleaned_row['Amount'] = float(cleaned_row['Amount'])
                except (TypeError, ValueError):
                    cleaned_row['Amount'] = 0.0

                expenses.append(cleaned_row)
    except Exception as e:
        print(f"Error loading file: {e}")
    return expenses


def save_expenses(file_path, expenses):
    """
    Save the list of expenses to a CSV file.
    Each expense should be a dictionary with:
    Date, Category, Amount, Description
    """
    directory = os.path.dirname(file_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(expenses)
    except Exception as e:
        print(f"Error saving file: {e}")
