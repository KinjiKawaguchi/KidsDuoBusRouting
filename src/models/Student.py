class Student:
    _node_id = 0
    
    def __init__(self, name, grade, pickup_point, dismissal_time):
        self.__id = Student._node_id
        self.__name = name
        self.__grade = grade
        self.__pickup_point = pickup_point
        self.__dismissal_time = dismissal_time
        Student._node_id += 1
        
    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_grade(self):
        return self.__grade

    def get_pickup_point(self):
        return self.__pickup_point

    def get_dismissal_time(self):
        return self.__dismissal_time
    
    def set_id(self, id):
        self.__id = id
        
    def set_name(self, name):
        self.__name = name

    def set_grade(self, grade):
        self.__grade = grade

    def set_pickup_point(self, pickup_point):
        self.__pickup_point = pickup_point

    def set_dismissal_time(self, dismissal_time):
        self.__dismissal_time = dismissal_time
