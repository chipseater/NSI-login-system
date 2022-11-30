from .db_func import db_func
import sqlite3


class TodoManager:
    def __init__(self):
        self.conn = sqlite3.connect('database/todos.db')

    @db_func
    def get_todos(self, cursor):
        cursor.execute(f"""
            CREATE OR REPLACE TABLE todos (
                id integer primary key,
                owner integer,
                name varchar(255),
                descr text,
                date text default unixepoch(),
                priority integer,
                done integer,
            )
        """)
