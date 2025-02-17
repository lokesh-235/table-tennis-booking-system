from api.users import users
import sqlite3
class admin(users):
    def __init__(self):
        super().__init__()

    
    def create_admin_table(self):
        query="""CREATE TABLE IF NOT EXISTS admin(adminname TEXT PRIMARY KEY , adminpass TEXT)"""
        self.cursor.execute(query)
        print('admin table created')
    
    

    def create_table_bookings_table(self):
        query="""CREATE TABLE IF NOT EXISTS table_bookings(tableno INTEGER PRIMARY KEY , status TEXT)"""
        self.cursor.execute(query)
        print('bookings table is created')


    def create_transaction_table(self):
        query="""CREATE TABLE IF NOT EXISTS transactions(tid INTEGER PRIMARY KEY , FOREIGN KEY (tableno) REFERENCES table_bookings(tableno) , FOREIGN KEY (username) REFERENCES users(username))"""   
        self.cursor.execute(query)
        print('transactions table is created')


    def select_all_users(self):
        query="""SELECT * from users ; """
        self.cursor.execute(query)
        res=self.cursor.fetchall()
        return res
    
    def select_all_transactions(self):
        query="""SELECT * from transactions """
        self.cursor.execute(query)
        res=self.cursor.fetchall()
        return res
    
    def add_table(self,tableno,status):
        query="""SELECT * FROM table_bookings WHERE tableno=? """
        self.cursor.execute(query,(tableno,))
        res=self.cursor.fetchone()
        if res:
            print("table already exists")
        else:
            query="""INSERT INTO table_bookings(tableno,status) VALUES(?,?) """
            self.cursor.execute(query,(tableno,status))
            self.conn.commit()
            print('table added')
    
    def select_all_tables(self):
        query="""SELECT * FROM table_bookings ; """
        self.cursor.execute(query)
        res=self.cursor.fetchall()
        return res
    def total_no_of_tables(self):
        query="""SELECT max (tableno) from table_bookings"""
        self.cursor.execute(query)
        res=self.cursor.fetchone()
        return res
    def select_table_status(self,tableno):
        query="""SELECT status FROM table_bookings WHERE tableno=? """
        self.cursor.execute(query,(tableno,))
        res=self.cursor.fetchone()
        return res
    
    def select_empty_tables(self):
        query="""SELECT tableno from table_bookings WHERE status=?"""
        self.cursor.execute(query,('empty',))
        res=self.cursor.fetchall()
        return res

    def update_table_status(self, tableno, status, date_booked, from_time, to_time):
        query = """
        UPDATE table_bookings 
        SET status = ?, date_booked = ?, from_time = ?, to_time = ? 
        WHERE tableno = ?
        """
        params = (status, date_booked, from_time, to_time, tableno)
        self.cursor.execute(query, params) 
        self.conn.commit()
        return 'successfully updated'
    def total_no_of_tables(self):
        query="""SELECT max (tableno) from table_bookings """
        self.cursor.execute(query)
        res=self.cursor.fetchone()
        return res
    def delete_table(self,tableno):
        query="""DELETE FROM table_bookings WHERE tableno=? """
        self.cursor.execute(query,(tableno,))
        self.conn.commit()
        print('table deleted')
    
    def add_transaction(self, tid, tableno, username):
        try:
            # Check if transaction exists
            query = "SELECT 1 FROM transactions WHERE tid=?"
            self.cursor.execute(query, (tid,))
            if self.cursor.fetchone():
                print("Transaction already exists")
                return

            # Validate table and check availability in one query
            query = "SELECT status FROM table_bookings WHERE tableno=?"
            self.cursor.execute(query, (tableno,))
            table_status = self.cursor.fetchone()

            if not table_status:
                print("Table does not exist")
                return
            if table_status[0] == "booked":
                print("Table is already booked")
                return

            # Check if user exists
            query = "SELECT 1 FROM users WHERE username=?"
            self.cursor.execute(query, (username,))
            if not self.cursor.fetchone():
                print("User does not exist")
                return

            # Insert transaction & update table status in a transaction
            self.conn.execute("BEGIN")
            self.cursor.execute("INSERT INTO transactions (tid, tableno, username) VALUES (?, ?, ?)", (tid, tableno, username))
            self.cursor.execute("UPDATE table_bookings SET status='booked' WHERE tableno=?", (tableno,))
            self.conn.commit()
            print("Transaction added, table booked")
        
        except sqlite3.Error as e:
            self.conn.rollback()
            print("Table is not booked", e)
    
    