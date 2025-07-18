#To interact with the database

import mysql.connector
from contextlib import contextmanager
from backend.logging_setup import setup_logger

logger = setup_logger('db_helper')



@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Rayhaan13!",
        database="expense_manager"
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor

    if commit:
        connection.commit()

    cursor.close()
    connection.close()

# def fetch_all_records():
#     with get_db_cursor() as cursor:
#         cursor.execute("select * from expenses;")
#         expenses=cursor.fetchall()
#         return expenses


def fetch_expense_for_date(expense_date):
    logger.info(f"fetch_expense_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses=cursor.fetchall()
        return expenses

def insert_expense(expense_date,amount,category,notes):
    logger.info(f"insert_expense_for_date called with date:{expense_date},amount:{amount},category:{category},notes:{notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
                       )

def delete_expense(expense_date):
    logger.info(f"delete_expense called with expense_date:{expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))

def fetch_expense_summary_by_category(start_date,end_date):
    logger.info(f"fetch_expense_summary called with start_date:{start_date},end_date:{end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT category, SUM(amount) as total 
               FROM expenses WHERE expense_date
               BETWEEN %s and %s  
               GROUP BY category;''',
            (start_date, end_date)
        )
        data=cursor.fetchall()
        return data

def fetch_expense_summary_by_month():
    logger.info(f"fetch_expense_summary_by_month called")
    with get_db_cursor() as cursor:
        cursor.execute('''SELECT MONTH(expense_date) as expense_month,
            MONTHName(expense_date) AS Month ,SUM(amount) as Total
            FROM expenses 
            GROUP BY expense_month,Month
            ORDER BY expense_month''')
        data =cursor.fetchall()
        return data

if __name__ == '__main__':
    # fetch_expense_for_date('2024-08-01')

    # summary=fetch_expense_summary_by_category("2024-08-01","2024-08-05")
    # for expense in summary:
    #     print(expense)

    data = fetch_expense_summary_by_month()
    for expense in data:
        print(expense)
