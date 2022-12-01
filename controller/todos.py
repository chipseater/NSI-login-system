from .db_func import db_func
import sqlite3


class TodoManager:
    def __init__(self):
        self.conn = sqlite3.connect('database/todos.db')

    @db_func
    def createTable(self, cursor):
        cursor.execute(f"""
            CREATE TABLE todos (
                id integer primary key,
                name varchar(255),
                important integer,
                done integer default FALSE,
                owner integer,
                date datetime default current_timestamp
            )
        """)
    
    @db_func
    def createTodo(self, cursor, user_id, name, important):
        cursor.execute(f"""
            INSERT INTO todos (owner, name, important) VALUES (
                "{user_id}", "{name}", "{important}"
            )
        """)

        res = cursor.execute(f"""
            SELECT * FROM todos WHERE owner = {user_id}
        """).fetchone()

        return {
            'todo': res
        }

    
    @db_func
    def getUserTodos(self, cursor, user_id):
        res = cursor.execute(f"""
            SELECT * FROM todos WHERE owner = {user_id}
        """).fetchall()

        print(res)

        return {
            'todos': res
        }
