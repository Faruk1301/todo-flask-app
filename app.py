from flask import Flask, render_template, request
import pyodbc
import os

app = Flask(__name__)

# Helper function to get DB connection
def get_db_connection():
    return pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={os.environ.get("DB_SERVER")};'
        f'DATABASE={os.environ.get("DB_NAME")};'
        f'UID={os.environ.get("DB_USER")};'
        f'PWD={os.environ.get("DB_PASSWORD")}',
        autocommit=True
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    employee = None
    if request.method == 'POST':
        emp_id = request.form['emp_id']
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employees WHERE id = ?", emp_id)
            row = cursor.fetchone()
            if row:
                employee = {
                    'id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'phone': row[3],
                    'position': row[4],
                    'department': row[5]
                }
        except Exception as e:
            employee = {'error': str(e)}
    return render_template('index.html', employee=employee)
