# Todo Flask App (Codespaces Ready)

This is a simple Flask app connected to Azure SQL Database.  
It is configured to run directly in GitHub Codespaces.

## How to run in Codespaces

1. Create a Codespace from this repo.
2. In terminal, set your SQL connection string:
```bash
export SQL_CONNECTION_STRING="Driver={ODBC Driver 17 for SQL Server};Server=tcp:<your_server>.database.windows.net;Database=tododb;Uid=sqladmin;Pwd=<password>;Encrypt=yes;"
```
3. Run the app:
```bash
python app.py
```
4. Open the forwarded port (5000) in Codespaces to access the app.
