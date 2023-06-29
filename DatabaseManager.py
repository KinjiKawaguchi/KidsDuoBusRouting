import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Places (
                name TEXT UNIQUE,
                address TEXT UNIQUE
            );
        ''')
        self.conn.commit()

    def check_place_exists(self, name, address):
        self.cursor.execute("SELECT * FROM Places WHERE name = ? OR address = ?", (name, address))
        return self.cursor.fetchone() is not None

    def add_place(self, name, address):
        try:
            self.cursor.execute("INSERT INTO Places (name, address) VALUES (?, ?)", (name, address))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"Error: '{name}' or '{address}' already exists in the database.")
