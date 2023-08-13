import sqlite3


class PlaceDatabaseManager:
    # Constants for columns
    ORIGIN_ID = 1
    STUDENT_DATA_COLUMN_NUM = 3
    PICKUP_POINT_DATA_COLUMN_NUM = 4
    ROUTE_SEGMENT_DATA_COLUMN__NUM = 5
    
    PP_TABLE_NAME = "pickup_point"
    RS_TABLE_NAME = "route_segment"
    
    PP_ID_COLUMN = 0
    PP_NAME_COLUMN = 1
    PP_ADDRESS_COLUMN = 2
    PP_IS_ORIGIN_COLUMN = 3
    PP_CAN_WAIT_COLUMN = 4

    RS_ID_COLUMN = 0
    RS_ORIGIN_ID_COLUMN = 1
    RS_DESTINATION_ID_COLUMN = 2
    RS_DURATION_COLUMN = 3
    RS_DISTANCE_COLUMN = 4

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        # Create pickup_point table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pickup_point (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                address TEXT,
                is_origin BOOLEAN,
                can_wait BOOLEAN,
                UNIQUE (name, address)
            );
        ''')

        # Create route_segment table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS route_segment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                origin_id INTEGER,
                destination_id INTEGER,
                duration REAL,  -- Time in seconds
                distance REAL,  -- Distance in meters
                FOREIGN KEY (origin_id) REFERENCES pickup_point(id),
                FOREIGN KEY (destination_id) REFERENCES pickup_point(id)
            );
        ''')
        self.conn.commit()
        
    # -------------------------(Common Table Operations)--------------------------------
    def get_all_data(self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        return self.cursor.fetchall()
    
    def is_table_empty(self, table_name):
        self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        return self.cursor.fetchone()[0] == 0

    # ------------------------(PickupPoint Table Operations)--------------------------------

    def is_pickup_point_exists(self, id=None, name=None, address=None):
        if id:
            self.cursor.execute("SELECT * FROM pickup_point WHERE id = ?", (id,))
        elif name and address:
            self.cursor.execute(
                "SELECT * FROM pickup_point WHERE name = ? AND address = ?", (name, address))
        else:
            raise ValueError("Either id or both name and address must be provided.")
        return self.cursor.fetchone() is not None

    def add_pickup_point(self, name, address, can_wait, is_origin=False):
        can_wait_value = 1 if can_wait == "TRUE" else 0
        is_origin_value = 1 if is_origin == "TRUE" else 0
        try:
            self.cursor.execute(
                "INSERT INTO pickup_point (name, address, is_origin, can_wait) VALUES (?, ?, ?, ?)",
                (name, address, is_origin_value, can_wait_value))
            self.conn.commit()
            self.cursor.execute(
                "SELECT * FROM pickup_point WHERE name = ? AND address = ?", (name, address))
            return self.cursor.fetchone()
        except sqlite3.IntegrityError:
            print(f"Error: '{name}' or '{address}' already exists in the database.")
            return False

    def get_pickup_point(self, id):
        self.cursor.execute("SELECT * FROM pickup_point WHERE id = ?", (id,))
        return self.cursor.fetchone()

    def get_all_pickup_points(self):
        self.cursor.execute("SELECT * FROM pickup_point")
        return self.cursor.fetchall()

    def update_pickup_point(self, id, new_name, new_address, new_can_wait):
        self.cursor.execute(
            "UPDATE pickup_point SET name = ?, address = ?, can_wait = ? WHERE id = ?",
            (new_name, new_address, new_can_wait, id))
        self.conn.commit()
        # Return the updated data
        self.cursor.execute("SELECT * FROM pickup_point WHERE id = ?", (id,))
        return self.cursor.fetchone()

    def delete_pickup_point(self, id):
        # Fetch the data before deletion
        self.cursor.execute("SELECT * FROM pickup_point WHERE id = ?", (id,))
        data = self.cursor.fetchone()
        self.cursor.execute("DELETE FROM pickup_point WHERE id = ?", (id,))
        self.conn.commit()
        # Return the deleted data
        return data

    def count_pickup_points(self):
        self.cursor.execute("SELECT COUNT(*) FROM pickup_point")
        return self.cursor.fetchone()[0]

    # ------------------------(RouteSegment Table Operations)--------------------------------
    def is_route_segment_exists(self, origin_id, destination_id):
        self.cursor.execute(
            "SELECT * FROM route_segment WHERE origin_id = ? AND destination_id = ?", (origin_id, destination_id))
        return self.cursor.fetchone() is not None

    def add_route_segment(self, origin_id, destination_id, duration, distance):
        self.cursor.execute(
            "INSERT INTO route_segment (origin_id, destination_id, duration, distance) VALUES (?, ?, ?, ?)",
            (origin_id, destination_id, duration, distance))
        self.conn.commit()
        self.cursor.execute(
            "SELECT * FROM route_segment WHERE origin_id = ? AND destination_id = ?", (origin_id, destination_id))
        return self.cursor.fetchone()

    def get_route_segment(self, route_segment_id=None, pickup_point_id=None, origin_id=None, destination_id=None):
        if route_segment_id:
            self.cursor.execute(
                "SELECT * FROM route_segment WHERE id = ?", (route_segment_id,))
            return self.cursor.fetchone()
        elif destination_id and origin_id:
            self.cursor.execute(
                "SELECT * FROM route_segment WHERE origin_id = ? AND destination_id = ?",
                (origin_id, destination_id))
            return self.cursor.fetchall()
        elif pickup_point_id:
            self.cursor.execute(
                "SELECT * FROM route_segment WHERE origin_id = ? OR destination_id = ?",
                (pickup_point_id, pickup_point_id))
            return self.cursor.fetchall()
        else:
            print("Error calling get_route_segment method.")
            return None

    def get_all_route_segment(self):
        self.cursor.execute("SELECT * FROM route_segment")
        return self.cursor.fetchall()

    def update_route_segment(self, route_segment_id, new_duration, new_distance):
        self.cursor.execute(
            "UPDATE route_segment SET duration = ?, distance = ? WHERE id = ?",
            (new_duration, new_distance, route_segment_id))
        self.conn.commit()
        self.cursor.execute(
            "SELECT * FROM route_segment WHERE id = ?", (route_segment_id,))
        return self.cursor.fetchone()

    def delete_route_segments(self, route_segment_id=None, origin_id=None, destination_id=None):
        if route_segment_id:
            self.cursor.execute("SELECT * FROM route_segment WHERE id = ?", (route_segment_id,))
            deleted_data = self.cursor.fetchone()
            self.cursor.execute("DELETE FROM route_segment WHERE id = ?", (route_segment_id,))
        elif origin_id and destination_id:
            self.cursor.execute("SELECT * FROM route_segment WHERE origin_id = ? AND destination_id = ?",
                                (origin_id, destination_id))
            deleted_data = self.cursor.fetchone()
            self.cursor.execute("DELETE FROM route_segment WHERE origin_id = ? AND destination_id = ?",
                                (origin_id, destination_id))
        else:
            print("Error: Incorrect call to delete_route_segment.")
            return None

        self.conn.commit()
        return deleted_data

    def close(self):
        self.conn.close()
        