from flask import Flask, render_template, request
import pyodbc

app = Flask(__name__)

# Full Azure SQL connection string
CONN_STR = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=tcp:toserver.database.windows.net,1433;"
    "Database=employee-db;"
    "Uid=azureuser;"
    "Pwd=aA@&1301278901;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

# Helper function to get DB connection safely
def get_db_connection():
    try:
        conn = pyodbc.connect(CONN_STR, autocommit=True)
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
            emp_id = int(request.form['emp_id'])
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

@app.route('/test-db')
def test_db():
    conn = get_db_connection()
    if not conn:
        return "Database connection failed! Check connection string and firewall."
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 5 * FROM employees")
        rows = cursor.fetchall()
        conn.close()
        return f"Rows fetched: {len(rows)}"
    except Exception as e:
        return f"Database query failed: {e}"

@app.route('/health')
def health():
    return "App is running!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
