class User:
    def __init__(self, db_id, username, password_hash, encrypted_api_key, keep_logged_in, is_logged_in, created_at,
                 updated_at):
        self.__db_id = db_id
        self.__username = username
        self.__password_hash = password_hash
        self.__encrypted_api_key = encrypted_api_key
        self.__keep_logged_in = keep_logged_in
        self.__is_logged_in = is_logged_in
        self.__created_at = created_at
        self.__updated_at = updated_at
        
    def get_db_id(self):
        return self.__db_id
    
    def get_username(self):
        return self.__username
    
    def get_password_hash(self):
        return self.__password_hash
    
    def get_encrypted_api_key(self):
        return self.__encrypted_api_key
    
    def get_keep_logged_in(self):
        return self.__keep_logged_in
    
    def get_is_logged_in(self):
        return self.__is_logged_in
    
    def get_created_at(self):
        return self.__created_at
    
    def get_updated_at(self):
        return self.__updated_at
    
    def set_name(self, username):
        self.__username = username
        
    def set_password_hash(self, password_hash):
        self.__password_hash = password_hash
        
    def set_encrypted_api_key(self, encrypted_api_key):
        self.__encrypted_api_key = encrypted_api_key
        
    def set_keep_logged_in(self, keep_logged_in):
        self.__keep_logged_in = keep_logged_in
        
    def set_is_logged_in(self, is_logged_in):
        self.__is_logged_in = is_logged_in
        
    def set_created_at(self, created_at):
        self.__created_at = created_at
        
    def set_updated_at(self, updated_at):
        self.__updated_at = updated_at
        