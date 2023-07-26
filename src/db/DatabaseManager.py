import sqlite3


class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS places (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                address TEXT,
                UNIQUE (name, address) 
            );
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS route_segments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                origin_id INTEGER,
                destination_id INTEGER,
                duration REAL,  -- 単位：秒
                distance REAL,  -- 単位：メートル
                FOREIGN KEY (origin_id) REFERENCES places(id),
                FOREIGN KEY (destination_id) REFERENCES places(id)
            );
        ''')

        self.conn.commit()

    def is_pickup_point_exits(self, id):
        self.cursor.execute("SELECT * FROM places WHERE id = id", (id,))
        return self.cursor.fetchone() is not None

    def is_table_empty(self):
        self.cursor.execute("SELECT COUNT(*) FROM places")
        return self.cursor.fetchone()[0] == 0

    def add_pickup_point(self, name, address):
        try:
            self.cursor.execute(
                "INSERT INTO places (name, address) VALUES (?, ?)", (name, address))
            self.conn.commit()

            # Return the added data
            self.cursor.execute(
                "SELECT * FROM places WHERE name = ? AND address = ?", (name, address))
            return self.cursor.fetchone()
        except sqlite3.IntegrityError:
            print(
                f"Error: '{name}' or '{address}' already exists in the database.")
            return False

    def get_pickup_point(self, id):
        self.cursor.execute("SELECT * FROM places WHERE id = ?", (id,))
        return self.cursor.fetchone()

    def get_all_pickup_points(self):
        self.cursor.execute("SELECT * FROM places")
        return self.cursor.fetchall()

    def update_pickup_point(self, id, new_name, new_address):
        self.cursor.execute(
            "UPDATE places SET name = ?, address = ? WHERE id = ?", (new_name, new_address, id))
        self.conn.commit()
        # Return the updated data
        self.cursor.execute("SELECT * FROM places WHERE id = ?", (id,))
        return self.cursor.fetchone()

    def delete_pickup_point(self, id):
        # Fetch the data before deletion
        self.cursor.execute("SELECT * FROM places WHERE id = ?", (id,))
        data = self.cursor.fetchone()
        self.cursor.execute("DELETE FROM places WHERE id = ?", (id,))
        self.conn.commit()
        # Return the deleted data
        return data

    def count_pickup_point(self):
        self.cursor.execute("SELECT COUNT(*) FROM places")
        return self.cursor.fetchone()[0]
    
# ------------------------(RouteSegmentTable)-------------------------------------------

    def is_route_segment_exits(self, origin_id, destination_id):
        pass

    def add_route_segment(self, added_id, comparing_id, duration, distance):
        self.cursor.execute("INSERT INTO route_segments (origin_id, destination_id, duration, distance) VALUES (?, ?, ?, ?)",
                            (added_id, comparing_id, duration, distance))
        self.conn.commit()
        return self.cursor.fetchone()

    def get_route_segment(self, origin_id, destination_id):
        self.cursor.execute(
            "SELECT * FROM route_segment WHERE origin_id = ? AND destination_id = ?", (origin_id, destination_id))
        return self.cursor.fetchone()
    
    def get_all_route_segments(self):
        self.cursor.execute("SELECT * FROM route_segment")
        return self.cursor.fetchall()

    def update_route_segment(self, origin_id, destination_id, new_origin_id, new_destination_id, new_duration, new_distance):
        self.cursor.execute("UPDATE route_segment SET origin_id = ?, destination_id = ?, duration = ?, distance = ? WHERE origin_id = ? AND destination_id = ?",
                            (new_origin_id, new_destination_id, new_duration, new_distance, origin_id, destination_id))
        updated_data = self.cursor.fetchone()
        return updated_data

    def delete_route_segment(self, id):
        self.cursor.execute("DELETE FROM route_segment WHERE id = ?", (id,))
        deleted_data = self.cursor.fetchone()
        return deleted_data
    
    def delete_route_segment(self, origin_id, destination_id):
        self.cursor.execute("DELETE FROM route_segment WHERE origin_id = ? AND destination_id = ?", (origin_id, destination_id))
        deleted_data = self.cursor.fetchone()
        return deleted_data
    