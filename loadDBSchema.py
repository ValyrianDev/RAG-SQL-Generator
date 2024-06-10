import logging
import re
import json
import os
from dbConnection import create_connection
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(filename='dbAgent.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')


def fetch_and_save_schema():
    # Load credentials from .env
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    wallet_location = os.getenv("DB_WALLET_LOCATION")
    config_dir = os.getenv("DB_CONFIG_DIR")
    dsn = os.getenv("DB_DSN")
    schema_owner = os.getenv("DB_SCHEMA")

    # Set output file
    output_file = 'schema_info.json'

    # Create the connection
    connection = create_connection(username, password, wallet_location, config_dir, dsn)

    def get_table_ddl_with_comments(table_name):
        ddl_query = f"""
        SELECT DBMS_METADATA.GET_DDL('TABLE', '{table_name}') AS DDL FROM DUAL
        """
        comment_query = f"""
        SELECT COLUMN_NAME, COMMENTS
        FROM ALL_COL_COMMENTS
        WHERE TABLE_NAME = '{table_name}'
        """
        table_comment_query = f"""
        SELECT COMMENTS
        FROM ALL_TAB_COMMENTS
        WHERE TABLE_NAME = '{table_name}'
        """

        with connection.cursor() as cursor:
            # Fetch the DDL
            cursor.execute(ddl_query)
            ddl_result = cursor.fetchone()[0].read()

            # Fetch the column comments
            cursor.execute(comment_query)
            column_comments = cursor.fetchall()

            # Fetch the table comments
            cursor.execute(table_comment_query)
            table_comment = cursor.fetchone()

        return ddl_result, column_comments, table_comment

    def get_all_tables():
        tables_query = f"""
        SELECT TABLE_NAME
        FROM ALL_TABLES
        WHERE OWNER = '{schema_owner}'
        """
        with connection.cursor() as cursor:
            cursor.execute(tables_query)
            tables = cursor.fetchall()
        return [table[0] for table in tables]

    def parse_table_ddl(ddl, column_comments, table_comment):
        table_name = extract_table_name(ddl)
        columns = extract_columns(ddl)
        constraints = extract_constraints(ddl)
        return {
            "Table": table_name,
            "Columns": columns,
            "Constraints": constraints,
            "Column Comments": {col[0]: col[1] for col in column_comments if col[1] is not None},
            "Table Comment": table_comment[0] if table_comment else None
        }

    def extract_table_name(ddl):
        match = re.search(r'TABLE "(\w+)"\."(\w+)"', ddl)
        return match.group(2) if match else None

    def extract_columns(ddl):
        matches = re.findall(r'"(\w+)" \w+', ddl)
        return ', '.join(matches) if matches else None

    def extract_constraints(ddl):
        constraints = []
        matches = re.findall(r'CONSTRAINT "(\w+)" (\w+ \([\w, ]+\))', ddl)
        for match in matches:
            constraints.append(f"{match[0]}: {match[1]}")
        return '; '.join(constraints) if constraints else None

    # Fetch and parse DDL and comments for all tables
    all_tables = get_all_tables()
    parsed_tables = []

    for table_name in all_tables:
        ddl, column_comments, table_comment = get_table_ddl_with_comments(table_name)
        parsed_ddl = parse_table_ddl(ddl, column_comments, table_comment)
        parsed_tables.append(parsed_ddl)

    # Write the parsed tables info to a JSON file
    with open(output_file, 'w') as json_file:
        json.dump(parsed_tables, json_file, indent=4)

    # Print success message
    print("Database Schema has been saved")

    # Close the connection
    connection.close()
