python
from flask import Flask, render_template, request
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(_name_)

conn = pyodbc.connect(
    f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={os.getenv("DB_SERVER")};DATABASE={os.getenv("DB_NAME")};UID={os.getenv("DB_USER")};PWD={os.getenv("DB_PASSWORD")}'
)

@app.route('/', methods=['GET', 'POST'])
def index():
    employee = None
    if request.method == 'POST':
        emp_id = request.form['emp_id']
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE id = ?", emp_id)
        row = cursor.fetchone()
        if row:
            employee = {
                'id': row.id,
                'name': row.name,
                'email': row.email,
                'phone': row.phone,
                'position': row.position,
                'department': row.department
            }
    return render_template('index.html', employee=employee)

if _name_ == '_main_':
    app.run(debug=True)

