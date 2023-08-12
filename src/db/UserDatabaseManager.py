import sqlite3


class UserDatabaseManager:
    """Handles operations related to the user database."""

    USERS_TABLE_NAME = "users"

    USERS_ID_COLUMN = 0
    USERS_USERNAME_COLUMN = 1
    USERS_PASSWORD_HASH_COLUMN = 2
    USERS_ENCRYPTED_API_KEY_COLUMN = 3
    USERS_KEEP_LOGGED_IN_COLUMN = 4
    USERS_IS_LOGGED_IN_COLUMN = 5
    USERS_CREATED_AT_COLUMN = 6
    USERS_UPDATED_AT_COLUMN = 7

    def __init__(self, db_name="user.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._initialize_database()

    def _initialize_database(self):
        """Creates necessary tables if they don't exist."""
        self._create_users_table()
        self._create_login_attempts_table()
        self._create_roles_table()
        self._create_user_roles_table()
        self.conn.commit()

    def _create_users_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            encrypted_api_key TEXT NOT NULL,
            keep_logged_in BOOLEAN DEFAULT FALSE,
            is_logged_in BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

    def _create_login_attempts_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_attempts (
            attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            success BOOLEAN,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        """)

    def _create_roles_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS roles (
            role_id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT UNIQUE NOT NULL
        )
        """)

    def _create_user_roles_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_roles (
            user_id INTEGER,
            role_id INTEGER,
            PRIMARY KEY (user_id, role_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (role_id) REFERENCES roles(role_id)
        )
        """)

    """-------------usersテーブル関連-------------"""
    def get_logged_in_user(self):
        """Fetches the currently logged in user."""
        self.cursor.execute("SELECT * FROM users WHERE is_logged_in = 1")
        return self.cursor.fetchone()

    def create_user(self, username, password_hash, encrypted_api_key, keep_logged_in):
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password_hash, encrypted_api_key, keep_logged_in) "
                "VALUES (?, ?, ?, ?)",
                (username, password_hash, encrypted_api_key, keep_logged_in)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print("Error: ユーザ名がすでに存在しています。")
            return False

    def read_user(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return self.cursor.fetchone()

    def is_user_exist(self, username):
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
        return self.cursor.fetchone()[0] == 1

    def logout(self):
        """Sets the logged in user's status to logged out."""
        self.cursor.execute("UPDATE users SET is_logged_in = 0 WHERE is_logged_in = 1")
        self.conn.commit()

    def login(self, username):
        self.cursor.execute("UPDATE users SET is_logged_in = 1 WHERE username = ?", (username,))
        self.conn.commit()

    """-------------共通関数-------------"""

    def is_table_empty(self, table_name):
        """Checks if a table is empty."""
        self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        return self.cursor.fetchone()[0] == 0

    def close(self):
        self.conn.close()
