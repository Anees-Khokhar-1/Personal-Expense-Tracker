import csv
import os

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
                # Convert Amount to float
                try:
                    row['Amount'] = float(row['Amount'])
                except ValueError:
                    row['Amount'] = 0.0
                expenses.append(row)
    except Exception as e:
        print(f"Error loading file: {e}")
    return expenses


def save_expenses(file_path, expenses):
    """
    Save the list of expenses to a CSV file.
    Each expense should be a dictionary with:
    Date, Category, Amount, Description
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['Date', 'Category', 'Amount', 'Description']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(expenses)
    except Exception as e:
        print(f"Error saving file: {e}")