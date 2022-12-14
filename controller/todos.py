from .db_func import db_func
import sqlite3


class TodoManager:
    def __init__(self):
        self.conn = sqlite3.connect('database/todos.db')
        self.conn.row_factory = self.dict_factory

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

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
        """).fetchall()

        return {
            'todo': res
        }

    
    @db_func
    def getUserTodos(self, cursor, user_id, allTodos=False):
        if not allTodos:
            all_string = 'AND done = 0'
        res = cursor.execute(f"""
            SELECT * FROM todos WHERE owner = {user_id} {all_string}
        """).fetchall()

        return {
            'todos': res
        }

    
    @db_func
    def updateTodo(self, cursor, user_id, id, name, important, done):
        res = cursor.execute(f"""
            UPDATE todos SET name = "{name}", done = {done}, important = {important} WHERE id = {id} AND owner = {user_id}
        """).fetchall()

        return {
            'todos': res
        }

    
    @db_func
    def deleteTodo(self, cursor, user_id, id):
        res = cursor.execute(f"""
            DELETE FROM todos WHERE id = {id} AND owner = {user_id}
        """).fetchall()

        return {
            'todos': res
        }
