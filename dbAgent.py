import oracledb
import pandas as pd
from dbConnection import create_connection
from dotenv import load_dotenv
import os

load_dotenv()


def read_sql_query(file_path):
    """Reads a SQL query from a file and removes the trailing semicolon if present."""
    with open(file_path, 'r') as file:
        query = file.read().strip()
    if query.endswith(';'):
        query = query[:-1]
    return query


def execute_sql_query(query):
    # Load credentials from .env
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    wallet_location = os.getenv("DB_WALLET_LOCATION")
    config_dir = os.getenv("DB_CONFIG_DIR")
    dsn = os.getenv("DB_DSN")

    # Create the connection
    connection = create_connection(username, password, wallet_location, config_dir, dsn)

    # Execute the query and fetch results
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

    # Close the connection
    connection.close()

    # Create a DataFrame for pretty printing
    df = pd.DataFrame(rows, columns=columns)

    # Save results to CSV
    df.to_csv('QueryResults.csv', index=False)
    print(f"Results saved to QueryResults.csv")

    return df

