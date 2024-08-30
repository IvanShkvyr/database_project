from random import randint
from sqlite3 import Connection, Error

from faker import Faker


TASKS_DICTIONARY = {
"Купити хліб": "Зайти до пекарні та купити свіжий хліб.",
"Забрати дітей з цирку": "Приїхати до цирку та забрати дітей після вистави.",
"Приготувати вечерю": "Зробити вечерю на всю сім'ю.",
"Полити квіти": "Полити квіти в горщиках на балконі.",
"Вивести собаку": "Вийти на прогулянку з собакою на 30 хвилин.",
"Заплатити за комунальні послуги": "",
"Піти до спортзалу": "Зайнятися фізичними вправами в спортзалі.",
"Прочитати книгу": "Прочитати кілька розділів книги перед сном.",
"Записатися до лікаря": "Зателефонувати до клініки та записатися на прийом.",
"Сходити до магазину": "Купити продукти на тиждень у супермаркеті.",
"Підписати документи": "Прочитати та підписати важливі документи для роботи.",
"Прибрати квартиру": "Пропилососити килими та витерти пил.",
"Відправити посилку": "",
"Заправити авто": "Зайти на заправку та заправити машину бензином.",
"Подзвонити батькам": "Зателефонувати батькам та дізнатися, як у них справи.",
"Забрати білизну з хімчистки": "Зайти до хімчистки та забрати одяг.",
"Запросити друзів на вечерю": "Організувати вечерю вдома та запросити друзів.",
"Сходити до перукаря": "Записатися та піти до перукаря для стрижки.",
"Сплатити за інтернет": "Оплатити рахунок за інтернет на наступний місяць.",
"Організувати поїздку": "Забронювати квитки для вихідних за містом."
}
SQL_INSERT_USERS = "INSERT INTO users (fullname, email) VALUES (?, ?);"
SQL_INSERT_STATUS = (
                    "INSERT INTO status (name) VALUES ('new'),"
                    "('in progress'), ('completed');"
                    )
SQL_INSERT_TASKS = (
                    "INSERT INTO tasks (title, descriptions, status_id,"
                    " user_id) VALUES (?, ?, ?, ?);"
                    )

fake_data = Faker(['uk_UA'])


def seed_database_tables(conn: Connection) -> None:
    """
    Seeds the database with initial data.

    This function inserts sample data into the users, status, and tasks tables.
    It creates 10 user entries with fake names and emails, populates the status
    table with predefined status values, and inserts tasks with random status
    and user IDs from the provided dictionaries and random values.

    Parameters:
    conn (sqlite3.Connection): The SQLite database connection object.

    Returns:
    None

    Exceptions:
    Error: Raised if there is an error executing any of the SQL statements.
    """
    curs = conn.cursor()

    try:
        for _ in range(10):
            curs.execute(
                         SQL_INSERT_USERS,
                         (fake_data.name(), fake_data.email())
                        )
        
        curs.execute(SQL_INSERT_STATUS)

        for i, j in TASKS_DICTIONARY.items():
            curs.execute(
                         SQL_INSERT_TASKS,
                        (i, j, randint(1, 3), randint(1, 10))
                        )

        conn.commit()
    except Error as err:
        print(f"Error seeding the database: {err}")
        conn.rollback()
