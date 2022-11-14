import sqlite3

con = sqlite3.connect('test.db')

cursor = con.cursor()

# cursor.execute("""
#     CREATE TABLE employees (
#         first text,
#         last text,
#         pay integer
#     )
# """)

con.commit()
con.close()
