from collections import defaultdict
from datetime import datetime

def summarize_by_category(expenses):
    """Return dict: category -> total amount"""
    summary = defaultdict(float)
    for e in expenses:
        summary[e['Category']] += float(e['Amount'])
    return dict(summary)

def total_expenses(expenses):
    return sum(float(e['Amount']) for e in expenses)

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

def format_currency(val):
    return f"${val:,.2f}"
