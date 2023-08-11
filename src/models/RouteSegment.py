class RouteSegment:
    _node_id = 0

    def __init__(self, db_id, origin_pickup_point, destination_pickup_point, duration, distance):
        self.__id = self._node_id
        self.__db_id = db_id
        self.__origin_pickup_point = origin_pickup_point
        self.__destination_pickup_point = destination_pickup_point
        self.__duration = duration
        self.__distance = distance
        self._node_id += 1

    def get_id(self):
        return self.__id

    def get_db_id(self):
        return self.__db_id

    def get_origin_id(self):
        return self.__origin_pickup_point

    def get_destination_id(self):
        return self.__destination_pickup_point

    def get_duration(self):
        return self.__duration

    def get_distance(self):
        return self.__distance

    def set_id(self, id):
        self.__id = id

    def set_db_id(self, db_id):
        self.__db_id = db_id

    def set_origin_pickup_point(self, origin_pickup_point):
        self.__origin_pickup_point = origin_pickup_point

    def set_destination_pickup_point(self, destination_pickup_point):
        self.__destination_pickup_point = destination_pickup_point

    def set_duration(self, duration):
        self.__duration = duration

    def set_distance(self, distance):
        self.__distance = distance
