from flask import Flask, render_template, request
import pyodbc
import os

app = Flask(__name__)

def get_db_connection():
    try:
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={os.environ.get("DB_SERVER")};'
            f'DATABASE={os.environ.get("DB_NAME")};'
            f'UID={os.environ.get("DB_USER")};'
            f'PWD={os.environ.get("DB_PASSWORD")}',
            autocommit=True
        )
        return conn
    except Exception as e:
        print("DB connection failed:", e)
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    employee = None
    error = None
    if request.method == 'POST':
        emp_id = request.form['emp_id']
        conn = get_db_connection()
        if conn:
            try:
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
                else:
                    error = "Employee not found."
            except Exception as e:
                error = f"Query failed: {e}"
            finally:
                conn.close()
        else:
            error = "Cannot connect to the database."
    return render_template('index.html', employee=employee, error=error)

@app.route('/health')
def health():
    return "App is running!"
