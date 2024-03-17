import csv
import logging
import mysql.connector
import pyodbc
import cx_Oracle
import teradatasql


class DatabaseConnector:
    def __init__(self, db_type, host, port, username, password, database):
        self.db_type = db_type
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        self.query_count = 0
        self.logger = logging.getLogger('DatabaseConnector')

    def connect(self):
        try:
            if self.db_type.lower() == 'mysql':
                self.connection = mysql.connector.connect(
                    host=self.host,
                    port=self.port,
                    user=self.username,
                    password=self.password,
                    database=self.database
                )
            elif self.db_type.lower() == 'sqlserver':
                connection_string = f"DRIVER={{SQL Server}};SERVER={self.host},{self.port};DATABASE={self.database};UID={self.username};PWD={self.password}"
                self.connection = pyodbc.connect(connection_string)
            elif self.db_type.lower() == 'oracle':
                self.connection = cx_Oracle.connect(
                    user=self.username,
                    password=self.password,
                    dsn=f"{self.host}:{self.port}/{self.database}"
                )
            elif self.db_type.lower() == 'teradata':
                self.connection = teradatasql.connect(
                    host=self.host,
                    user=self.username,
                    password=self.password
                )
            else:
                raise ValueError("Unsupported database type")

            self.cursor = self.connection.cursor()
        except Exception as e:
            self.logger.error(f"Error connecting to the database: {e}")

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.query_count = len(result)
            return result
        except Exception as e:
            self.logger.error(f"Error executing query: {e}")

    def save_to_csv(self, data, filename):
        try:
            with open(filename, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerows(data)
        except Exception as e:
            self.logger.error(f"Error saving to CSV: {e}")

    def get_query_count(self):
        return self.query_count

    def close_connection(self):
        try:
            if self.connection:
                self.connection.close()
        except Exception as e:
            self.logger.error(f"Error closing connection: {e}")


# Example usage:
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    db_connector = DatabaseConnector(
        'mysql', 'localhost', 3306, 'username', 'password', 'database_name')
    db_connector.connect()
    query_result = db_connector.execute_query('SELECT * FROM table_name')
    logging.info("Query Count: %s", db_connector.get_query_count())
    db_connector.save_to_csv(query_result, 'output.csv')
    db_connector.close_connection()


# Example usage:
db_connector = DatabaseConnector(
    'mysql', 'localhost', 3306, 'username', 'password', 'database_name')
db_connector.connect()
query_result = db_connector.execute_query('SELECT * FROM table_name')
print("Query Count:", db_connector.get_query_count())
db_connector.save_to_csv(query_result, 'output.csv')
db_connector.close_connection()


# MySQL example
mysql_connector = DatabaseConnector(
    'mysql', 'localhost', 3306, 'username', 'password', 'database_name')
mysql_connector.connect()
mysql_data = mysql_connector.execute_query('SELECT * FROM table_name')
print(mysql_data)
mysql_connector.close_connection()

# SQL Server example
sql_server_connector = DatabaseConnector(
    'sqlserver', 'localhost', '1433', 'username', 'password', 'database_name')
sql_server_connector.connect()
sql_server_data = sql_server_connector.execute_query(
    'SELECT * FROM table_name')
print(sql_server_data)
sql_server_connector.close_connection()

# Oracle example
oracle_connector = DatabaseConnector(
    'oracle', 'localhost', 1521, 'username', 'password', 'database_name')
oracle_connector.connect()
oracle_data = oracle_connector.execute_query('SELECT * FROM table_name')
print(oracle_data)
oracle_connector.close_connection()

# Teradata example
teradata_connector = DatabaseConnector(
    'teradata', 'localhost', None, 'username', 'password', None)
teradata_connector.connect()
teradata_data = teradata_connector.execute_query('SELECT * FROM table_name')
print(teradata_data)
teradata_connector.close_connection()


def compare_csv_files(file1, file2):
    with open(file1, 'r') as csv_file1, open(file2, 'r') as csv_file2:
        csv_reader1 = csv.reader(csv_file1)
        csv_reader2 = csv.reader(csv_file2)

        rows_file1 = list(csv_reader1)
        rows_file2 = list(csv_reader2)

        if rows_file1 == rows_file2:
            print("The two CSV files are identical.")
        else:
            print("The two CSV files are not identical.")
            print("Differences:")
            for row1, row2 in zip(rows_file1, rows_file2):
                if row1 != row2:
                    print(f"Row {rows_file1.index(row1) + 1}:")
                    for col1, col2 in zip(row1, row2):
                        if col1 != col2:
                            print(
                                f"   Column {row1.index(col1) + 1}: '{col1}' (file1) != '{col2}' (file2)")


# Example usage:
file1 = 'file1.csv'
file2 = 'file2.csv'
compare_csv_files(file1, file2)
