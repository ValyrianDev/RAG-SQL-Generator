from loadDBSchema import fetch_and_save_schema
from marqoIndex import setup_marqo_index
from marqoSearch import search_marqo
from LLM import generate_sql_query
from dbAgent import execute_sql_query, read_sql_query
from dotenv import load_dotenv

load_dotenv()


def main():
    first_time_setup = input("Would you like to refresh database schema information? (yes/no): ").strip().lower()

    # Only load DDL and create indexes for initial setup
    if first_time_setup == 'yes':
        fetch_and_save_schema()
        setup_marqo_index()

    # Always perform search and query generation
    user_query = input("Enter your query: ").strip()
    search_marqo(user_query)
    generate_sql_query(user_query)

    # Read and execute the SQL query
    sql_query = read_sql_query('generated_query.sql')
    df = execute_sql_query(sql_query)
    print(df.to_markdown())


if __name__ == "__main__":
    main()
