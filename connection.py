from contextlib import contextmanager
from sqlite3 import connect, Connection, Error
from typing import Generator


DATABASE_PATH = "tasks_db.sqlite"


@contextmanager
def create_connection(database_path: str) -> Generator[Connection, None, None]:
    """
    Context manager for creating or connecting to an SQLite database.

    This context manager establishes a connection to an SQLite database at the
    specified path. If the database does not exist, it will be created
    automatically.     The connection is automatically closed after use.

    Parameters:
    database_path (str): The path to the SQLite database file.

    Exceptions:
    Error: Raised if there is an error connecting to the database or executing
           queries.

    Usage:
    ```
    with create_connection('path_to_db.sqlite') as conn:
        # Perform database operations here
        pass
    ```
    """
    try:
        conn = connect(database_path)
        yield conn
    except Error as err:
        print(err)
        conn.rollback()
    finally:
        conn.close()
    