import sqlite3

from BusRouting import BusRouting
from GoogleMapsClient import GoogleMapsClient


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
            self.cursor.execute("INSERT INTO Places (name, address) VALUES (?, ?)", (name, address))
            self.conn.commit()
            
            # Return the added data
            self.cursor.execute("SELECT * FROM Places WHERE name = ? AND address = ?", (name, address))
            return self.cursor.fetchone()
        except sqlite3.IntegrityError:
            print(f"Error: '{name}' or '{address}' already exists in the database.")
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
        self.cursor.execute("UPDATE Places SET name = ?, address = ? WHERE id = ?", (new_name, new_address, id))
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

#------------------------(RouteSegmentTable)-------------------------------------------
    def checkBusRouteSegmentExitsIs(self, nameFrom, nameTo, addressFrom, addressTo):
        pass

    def addRouteSegment(self):
        
        google = GoogleMapsClient()
        
        self.conn.execute('''SELECT * FROM Places WHERE id = (SELECT MAX(id) FROM Places)''')
        addedData = self.cursor.fetchone()
        addedAddress = addedData[2]
        
        self.conn.execute('''SELECT * FROM Places WHERE id = 0''')
        comparisonData = self.cursor.fetchone()
        
        while comparisonData != addedData:
            comparisonAddress = comparisonData[2]
            time, distance = google.getTravelTime(comparisonAddress, addedAddress)
            self.cursor.execute('''INSERT INTO BusRouteSegment (FromId, ToId, Time, Distance) VALUES(?, ?, ?, ?)''', (comparisonData[0], addedData[0], time, distance))

            time, distance = google.getTravelTime(addedAddress, comparisonAddress)
            self.cursor.execute('''INSERT INTO BusRouteSegment (FromId, ToId, Time, Distance) VALUES(?, ?, ?, ?)''', (comparisonData[0], addedData[0], time, distance))

            i = 1
            while not(self.checkPlaceExistsIs(comparisonData[0]+ i)):
                i += 1
            self.conn.execute('''SELECT * FROM Places WHERE id = ?''',(comparisonData[0] + i,))
            comparisonData = self.cursor.fetchone()
            
        self.conn.commit()

    def updateRouteSegment(self, id):
        #WIP
        pass

    def deleteRouteSegment(self, id):
        #WIP
        pass
