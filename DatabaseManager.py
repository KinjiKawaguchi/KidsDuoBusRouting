import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Places (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                address TEXT UNIQUE
            );
        ''')
        self.conn.commit()

    def checkPlaceExistIs(self, name, address):
        self.cursor.execute("SELECT * FROM Places WHERE name = ? OR address = ?", (name, address))
        return self.cursor.fetchone() is not None

    def checkTableEmptyIs(self):
        self.cursor.execute("SELECT COUNT(*) FROM Places")
        return self.cursor.fetchone()[0] == 0

    def addPlace(self, name, address):
        try:
            self.cursor.execute("INSERT INTO Places (name, address) VALUES (?, ?)", (name, address))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"Error: '{name}' or '{address}' already exists in the database.")

    def deletePlace(self, id):
        self.cursor.execute("DELETE FROM Places WHERE id = ?", (id,))
        self.conn.commit()

    def updatePlace(self, id, new_name, new_address):
        self.cursor.execute("UPDATE Places SET name = ?, address = ? WHERE id = ?", (new_name, new_address, id))
        self.conn.commit()

    def getAllplaces(self):
        self.cursor.execute("SELECT * FROM Places")
        return self.cursor.fetchall()
