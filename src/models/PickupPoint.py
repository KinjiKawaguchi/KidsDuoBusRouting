class PickupPoint:
    _node_id = 0

    def __init__(self, db_id, name, address, is_origin, can_wait):
        self.__id = PickupPoint._node_id
        self.__db_id = db_id
        self.__name = name
        self.__address = address
        self.__is_origin = is_origin
        self.__can_wait = can_wait
        PickupPoint._node_id += 1
        
    def get_id(self):
        return self.__id
    
    def get_db_id(self):
        return self.__db_id
    
    def get_name(self):
        return self.__name
    
    def get_address(self):
        return self.__address
    
    def get_is_origin(self):
        return self.__is_origin
    
    def get_can_wait(self):
        return self.__can_wait
    
    def set_id(self, id):
        self.__id = id
        
    def set_db_id(self, db_id):
        self.__db_id = db_id
        
    def set_name(self, name):
        self.__name = name
        
    def set_address(self, address):
        self.__address = address
        
    def set_is_origin(self, is_origin):
        self.__is_origin = is_origin
        
    def set_can_wait(self, can_wait):
        self.__can_wait = can_wait
