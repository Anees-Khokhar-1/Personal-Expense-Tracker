from collections import defaultdict
from datetime import datetime

def summarize_by_category(expenses):
    """Return dict: category -> total amount"""
    summary = defaultdict(float)
    for e in expenses:
        category = e.get('Category') or "Uncategorized"
        summary[category] += float(e.get('Amount') or 0)
    return dict(sorted(summary.items()))

def total_expenses(expenses):
    return sum(float(e.get('Amount') or 0) for e in expenses)

def filter_by_month(expenses, year, month):
    """Return expenses that match year and month (ints)."""
    out = []
    for e in expenses:
        try:
            d = datetime.fromisoformat(e['Date'])
        except Exception:
            # If date not in ISO format, skip or attempt fallback
            continue
        if d.year == year and d.month == month:
            out.append(e)
    return out

def filter_by_category(expenses, category):
    """Return expenses that match category, case-insensitively."""
    category = category.strip().lower()
    return [e for e in expenses if e.get('Category', '').lower() == category]

def search_expenses(expenses, keyword):
    """Return expenses whose description or category contains the keyword."""
    keyword = keyword.strip().lower()
    return [
        e for e in expenses
        if keyword in e.get('Description', '').lower()
        or keyword in e.get('Category', '').lower()
    ]

def sort_expenses(expenses, sort_key):
    """Return a sorted copy of expenses based on a menu sort key."""
    if sort_key == "date_asc":
        return sorted(expenses, key=lambda e: e.get('Date', ''))
    if sort_key == "date_desc":
        return sorted(expenses, key=lambda e: e.get('Date', ''), reverse=True)
    if sort_key == "amount_asc":
        return sorted(expenses, key=lambda e: float(e.get('Amount') or 0))
    if sort_key == "amount_desc":
        return sorted(expenses, key=lambda e: float(e.get('Amount') or 0), reverse=True)
    if sort_key == "category":
        return sorted(expenses, key=lambda e: e.get('Category', '').lower())
    return list(expenses)

def format_currency(val):
    return f"Rs. {val:,.2f}"
