from sqlite3 import Error, Connection
from typing import List

from connection import create_connection, DATABASE_PATH
from seed import seed_database_tables


def execute_query (
                  conn: Connection,
                  sql_query: str
                 ) -> List[str]:
    """
    Executes a SQL statement to create a table in the SQLite database.

    This function takes a SQL statement for creating a table and executes it
    using the provided database connection. If the execution is successful,
    the changes are committed to the database. In case of an error, the changes
    are rolled back to maintain database consistency. The cursor used for
    executing the SQL statement is closed after use.

    Parameters:
    conn (sqlite3.Connection): The SQLite database connection object.
    create_table_query (str): The SQL statement to create a table.

    Returns:
    List[str]: The result of the query, if applicable. Otherwise, an empty list

    Exceptions:
    Error: Raised if there is an error executing the SQL statement.
    """
    try:
        curs = conn.cursor()
        curs.execute(sql_query)

        # Check if the query contains "SELECT"
        is_select_query = "SELECT" in sql_query

        # If the SQL query is a SELECT query, fetch all results from the cursor
        if is_select_query:
            results = curs.fetchall()
        
        # If the SQL query is not a SELECT query, commit the changes to the
        # database and set results to an empty list
        else:
            conn.commit()
            results = []
    
    except Error as err:
        print(err)
        conn.rollback()
        results = []

    finally:
        curs.close()

    return results



def execute_sql_script(script_path: str) -> List[str]:
    """
    Reads an SQL script file and returns a list of individual SQL statements.

    This function reads the contents of an SQL script file located at the
    specified path and splits it into individual SQL statements. Each statement
    is returned as a separate string in a list, with a semicolon ';' appended
    to each statement.

    Parameters:
    script_path (str): The path to the SQL script file.

    Returns:
    List[str]: A list of SQL statements extracted from the script file.
    """
    with open(script_path, 'r') as sql_file:
        sql_script = sql_file.read()
    
    # Split the script ';' to separate the SQL statments
    sql_statements = sql_script.split(';')

    # Add back the ';' at the end of each statement
    sql_stmts  = [txt.strip() + ';' for txt in sql_statements if txt.strip()]

    return sql_stmts


if __name__ == "__main__":
    tables_schema_def_path = "tables.sql"

    query_execution_comm_path = 'queries.sql'

    # Get lists of SQL 
    tables_schema_definitions = execute_sql_script(tables_schema_def_path)
    query_execution_commands = execute_sql_script(query_execution_comm_path)

    with create_connection(DATABASE_PATH) as my_conn:
        
        # Creating tables
        for table_schem in tables_schema_definitions:
            execute_query(my_conn, table_schem)

        # Populate tables with data
        seed_database_tables(my_conn)

        # Execute SQL queries against the database
        for query in query_execution_commands:
            print('============== QUERY ==============')
            print(query)
            print('______________ RESULT ______________')
            results = execute_query(my_conn, query)
            for result in results:
                print(result)
