import sqlite3

"""
fetchone() : 1つのデータを取得する。戻り値はNoneかタプル。
fetchall() : 全てのデータを取得する。戻り値は空のリスト([])かタプルのリスト。
"""

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
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

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS route_segments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                origin_id INTEGER,
                destination_id INTEGER,
                duration REAL,  -- 単位：秒
                distance REAL,  -- 単位：メートル
                FOREIGN KEY (origin_id) REFERENCES pickup_point(id),
                FOREIGN KEY (destination_id) REFERENCES pickup_point(id)
            );
        ''')

        self.conn.commit()

    def is_pickup_point_exists(self, id=None, name=None, address=None):
        if id is not None:
            self.cursor.execute("SELECT * FROM pickup_point WHERE id = ?", (id,))
        elif name is not None and address is not None:
            self.cursor.execute(
                "SELECT * FROM pickup_point WHERE name = ? AND address = ?", (name, address))
        else:
            raise ValueError("Either id or both name and address must be provided.")

        return self.cursor.fetchone() is not None

    def is_table_empty(self):
        self.cursor.execute("SELECT COUNT(*) FROM pickup_point")
        return self.cursor.fetchone()[0] == 0

    def add_pickup_point(self, name, address, can_wait, is_origin=False):
        can_wait = 1 if can_wait == "TRUE" else 0
        is_origin = 1 if is_origin == "TRUE" else 0

        try:
            self.cursor.execute(
                "INSERT INTO pickup_point (name, address, is_origin, can_wait) VALUES (?, ?, ?, ?)", (name, address, is_origin, can_wait))
            self.conn.commit()

            # nameとaddressは一意なので、改めて検索して最後に追加されたデータを取得する。
            self.cursor.execute(
                "SELECT * FROM pickup_point WHERE name = ? AND address = ?", (name, address))
            return self.cursor.fetchone()
        except sqlite3.IntegrityError:
            print(
                f"Error: '{name}' or '{address}' already exists in the database.")
            return False

    def get_pickup_point(self, id):
        self.cursor.execute("SELECT * FROM pickup_point WHERE id = ?", (id,))
        return self.cursor.fetchone()

    def get_all_pickup_points(self):
        self.cursor.execute("SELECT * FROM pickup_point")
        return self.cursor.fetchall()

    def update_pickup_point(self, id, new_name, new_address, new_can_wait):
        self.cursor.execute(
            "UPDATE pickup_point SET name = ?, address = ? , can_wait = ?, WHERE id = ?", (new_name, new_address, new_can_wait, id))
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

    def count_pickup_point(self):
        self.cursor.execute("SELECT COUNT(*) FROM pickup_point")
        return self.cursor.fetchone()[0]

    # ------------------------(RouteSegmentTable)-------------------------------------------

    def is_route_segment_exits(self, origin_id, destination_id):
        self.cursor.execute(
            "SELECT * FROM route_segments WHERE origin_id = ? AND destination_id = ?", (origin_id, destination_id))
        return self.cursor.fetchone() is not None

    def add_route_segment(self, added_id, comparing_id, duration, distance):
        self.cursor.execute(
            "INSERT INTO route_segments (origin_id, destination_id, duration, distance) VALUES (?, ?, ?, ?)",
            (added_id, comparing_id, duration, distance))
        self.conn.commit()
        return self.cursor.fetchone()

    def get_route_segment(self, pickup_point_id, destination_id=None):
        if destination_id is None:
            self.cursor.execute(
                "SELECT * FROM route_segments WHERE origin_id = ? OR destination_id = ?",
                (pickup_point_id, pickup_point_id))
            return self.cursor.fetchall()
        else:
            self.cursor.execute(
                "SELECT * FROM route_segments WHERE origin_id = ? AND destination_id = ?",
                (pickup_point_id, destination_id))
            return self.cursor.fetchone()

    def get_all_route_segments(self):
        self.cursor.execute("SELECT * FROM route_segments")
        return self.cursor.fetchall()

    def update_route_segment(self, id,  new_duration, new_distance):
        self.cursor.execute(
            "UPDATE route_segments SET  duration = ?, distance = ? WHERE id = ?",
            (new_duration, new_distance, id))
        updated_data = self.cursor.fetchone()
        return updated_data

    def delete_route_segment(self, id):
        self.cursor.execute("DELETE FROM route_segments WHERE id = ?", (id,))
        deleted_data = self.cursor.fetchone()
        return deleted_data

    def delete_route_segment(self, origin_id, destination_id):
        self.cursor.execute("DELETE FROM route_segments WHERE origin_id = ? AND destination_id = ?",
                            (origin_id, destination_id))
        deleted_data = self.cursor.fetchone()
        return deleted_data
