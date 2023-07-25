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

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS BusRouteSegment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                FromId INTEGER,
                ToId INTEGER,
                Time REAL,
                Distance REAL,
                FOREIGN KEY (FromId) REFERENCES Places(id),
                FOREIGN KEY (ToId) REFERENCES Places(id)
            );
        ''')

        self.conn.commit()

    def checkPlaceExistsIs(self, id):
        self.cursor.execute("SELECT * FROM Places WHERE id = id", (id,))
        return self.cursor.fetchone() is not None

    def checkTableEmptyIs(self):
        self.cursor.execute("SELECT COUNT(*) FROM Places")
        return self.cursor.fetchone()[0] == 0

    def addPlace(self, name, address):
        try:
            self.cursor.execute(
                "INSERT INTO Places (name, address) VALUES (?, ?)", (name, address))
            self.conn.commit()

            # Return the added data
            self.cursor.execute(
                "SELECT * FROM Places WHERE name = ? AND address = ?", (name, address))
            return self.cursor.fetchone()
        except sqlite3.IntegrityError:
            print(
                f"Error: '{name}' or '{address}' already exists in the database.")
            return False

    def deletePlace(self, id):
        # Fetch the data before deletion
        self.cursor.execute("SELECT * FROM Places WHERE id = ?", (id,))
        data = self.cursor.fetchone()
        self.cursor.execute("DELETE FROM Places WHERE id = ?", (id,))
        self.conn.commit()
        # Return the deleted data
        return data

    def updatePlace(self, id, new_name, new_address):
        self.cursor.execute(
            "UPDATE Places SET name = ?, address = ? WHERE id = ?", (new_name, new_address, id))
        self.conn.commit()
        # Return the updated data
        self.cursor.execute("SELECT * FROM Places WHERE id = ?", (id,))
        return self.cursor.fetchone()

    def getAllplaces(self):
        self.cursor.execute("SELECT * FROM Places")
        return self.cursor.fetchall()

    def getPickupPointNum(self):
        self.cursor.execute("SELECT COUNT(*) FROM Places")
        return self.cursor.fetchone()[0]
    
    def getPickupPoint(self, id):
        self.cursor.execute("SELECT * FROM Places WHERE id = ?", (id,))
        return self.cursor.fetchone()

# ------------------------(RouteSegmentTable)-------------------------------------------
    def checkBusRouteSegmentExitsIs(self, nameFrom, nameTo, addressFrom, addressTo):
        pass

    def addRouteSegment(self, addedId, comparisonId, time, distance):
        self.cursor.execute("INSERT INTO BusRouteSegment (FromId, ToId, Time, Distance) VALUES (?, ?, ?, ?)",
                            (addedId, comparisonId, time, distance))
        self.conn.commit()
        return self.cursor.fetchone()
    
    def getRouteSegment(self, id):
        pass
    
    def getRouteSegment(self, FromId, ToId):
        pass

    def updateRouteSegment(self, id):
        # WIP
        pass

    def deleteRouteSegment(self, id):
        # WIP
        pass
