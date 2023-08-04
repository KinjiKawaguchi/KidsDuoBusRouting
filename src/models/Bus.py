class Bus:
    _node_id = 0

    def __init__(self, name, max_passenger, driver_name, attendant_name):
        self.__id = Bus._node_id
        self.__name = name
        self.__max_passenger = max_passenger
        self.__driver_name_list = driver_name
        self.__attendant_name_list = attendant_name
        self.__student_list = []
        self.__route_list = []
        self.__departure_time_list = []
        self.__arrival_time_list = []
        Bus._node_id += 1

    def add_route(self, pickup_point, departure_time, arrival_time):
        self.__route_list.append(pickup_point)
        self.__departure_time_list.append(departure_time)
        self.__arrival_time_list.append(arrival_time)

    def add_student(self, student):
        self.__student_list.append(student)

    def remove_student(self, student):
        self.__student_list.remove(student)

    def get_id(self):
        return self.__id
    
    def get_name(self):
        return self.__name
    
    def get_max_passenger(self):
        return self.__max_passenger
    
    def get_driver_name_list(self):
        return self.__driver_name_list
    
    def get_attendant_name_list(self):
        return self.__attendant_name_list
    
    def get_student_list(self):
        return self.__student_list
    
    def get_route_list(self):
        return self.__route_list
    
    def get_departure_time_list(self):
        return self.__departure_time_list
    
    def get_arrival_time_list(self):
        return self.__arrival_time_list
    
    def set_id(self, id):
        self.__id = id
    
    def set_name(self, name):
        self.__name = name
        
    def set_max_passenger(self, max_passenger):
        self.__max_passenger = max_passenger
        
    def set_driver_name_list(self, driver_name_list):
        self.__driver_name_list = driver_name_list
    
    def set_attendat_name_list(self, attendant_name_list):
        self.__attendant_name_list = attendant_name_list
        
    def set_student_list(self, student_list):
        self.__student_list = student_list
    
    def set_route_list(self, route_list):
        self.__route_list = route_list
        
    def set_departure_time_list(self, departure_time_list):
        self.__departure_time_list = departure_time_list
    
    def set_arrival_time_list(self, arrival_time_list):
        self.__arrival_time_list = arrival_time_list
    