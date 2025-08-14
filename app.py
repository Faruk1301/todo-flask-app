from flask import Flask, render_template, request
import pyodbc
import os

app = Flask(__name__)

# Database connection using Azure App Service environment variables
conn = pyodbc.connect(
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
    return render_template('index.html', employee=employee)

if __name__ == "__main__":
    # Azure provides the PORT environment variable for the app
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

