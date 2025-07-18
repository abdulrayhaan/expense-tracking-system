from backend import db_helper
# import backend.db_helper as db_helper

def test_fetch_expense_for_date():
    expenses=db_helper.fetch_expense_for_date("2024-08-15")

    assert len(expenses)==1
    assert expenses[0]['amount']==10
    assert expenses[0]['category']=='Shopping'
    assert expenses[0]['notes'] == 'Bought potatoes'

def test_fetch_expense_for_invalid_date():
    expenses=db_helper.fetch_expense_for_date("2026-08-20")

    assert len(expenses)==0

def test_summary_for_invalid_range():
    summary=db_helper.fetch_expense_summary("2026-08-20","2027-09-10")

    assert len(summary)==0