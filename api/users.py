import sqlite3
class users:
    def __init__(self):
        self.conn=sqlite3.connect('bookings.db')
        self.cursor=self.conn.cursor()

        
    def create_table(self):
        query="""CREATE TABLE IF NOT EXISTS users ( username TEXT PRIMARY KEY , password TEXT )"""
        self.cursor.execute(query)
        self.conn.commit()

     
    def select_using_name(self , name):
        query=f"""SELECT * FROM users WHERE username = '{name}'"""
        self.cursor.execute(query)
        res=self.cursor.fetchone()
        return res

    def insert_record(self , username , password):
        query=f"""SELECT * FROM users where username = '{username}'"""
        self.cursor.execute(query)
        res=self.cursor.fetchone()
        if res:
            return 'username already exists'
        query=f"""INSERT INTO users VALUES ('{username}','{password}')"""
        self.cursor.execute(query)
        self.conn.commit()
        return 'successfully registered'

