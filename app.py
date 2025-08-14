from flask import Flask, render_template, request
import pyodbc
import os

app = Flask(__name__)

# Helper function to get DB connection safely
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
        print("Database connection failed:", e)
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    employee = None
    error = None
    if request.method == 'POST':
        try:
            emp_id = int(request.form['emp_id'])  # ensure integer for SQL query
            conn = get_db_connection()
            if conn:
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
                conn.close()
            else:
                error = "Cannot connect to the database."
        except ValueError:
            error = "Invalid ID. Please enter a number."
        except Exception as e:
            error = f"Error: {e}"

    return render_template('index.html', employee=employee, error=error)

# Route to test database connectivity
@app.route('/test-db')
def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 5 * FROM employees")
        rows = cursor.fetchall()
        return f"Rows fetched: {len(rows)}"
    except Exception as e:
        return f"Database connection failed: {e}"

# Health check route
@app.route('/health')
def health():
    return "App is running!"
