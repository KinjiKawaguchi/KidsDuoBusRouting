class Student:
    _node_id = 0
    
    def __init__(self, name, pickup_point, dismissal_time, no_bus=False):
        self.__id = Student._node_id
        self.__name = name
        self.__pickup_point = pickup_point
        self.__dismissal_time = dismissal_time
        self.__no_bus = no_bus
        Student._node_id += 1
        
    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_pickup_point(self):
        return self.__pickup_point

    def get_dismissal_time(self):
        return self.__dismissal_time

    def get_no_bus(self):
        return self.__no_bus
    
    def set_id(self, id):
        self.__id = id
        
    def set_name(self, name):
        self.__name = name

    def set_pickup_point(self, pickup_point):
        self.__pickup_point = pickup_point

    def set_dismissal_time(self, dismissal_time):
        self.__dismissal_time = dismissal_time

    def set_no_bus(self, no_bus):
        self.__no_bus = no_bus
