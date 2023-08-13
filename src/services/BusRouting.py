from src.models.Bus import Bus
from src.models.PickupPoint import PickupPoint
from src.models.RouteSegment import RouteSegment

from src.db.PlaceDatabaseManager import PlaceDatabaseManager


class BusRouting:
    def __init__(self):
        self.db = PlaceDatabaseManager("KidsDuoBusRouting.db")
        self.pickup_points = None
        self.route_segments = None
        self.students = None
        self.buses = []
        self.load_data()

    def load_data(self):
        # Instantiate pickup points
        self.pickup_points = self._instantiate_pickup_points()

        # Instantiate route segments
        self.route_segments = self._instantiate_route_segments()

    def _instantiate_pickup_points(self):
        return [PickupPoint(data[self.db.PP_ID_COLUMN], data[self.db.PP_NAME_COLUMN],
                            data[self.db.PP_ADDRESS_COLUMN], data[self.db.PP_IS_ORIGIN_COLUMN],
                            data[self.db.PP_CAN_WAIT_COLUMN])
                for data in self.db.get_all_pickup_points()]

    def _instantiate_route_segments(self):
        return [RouteSegment(data[self.db.RS_ID_COLUMN],
                             self._find_pickup_point_by_id(self.pickup_points, data[self.db.RS_ORIGIN_ID_COLUMN]),
                             self._find_pickup_point_by_id(self.pickup_points, data[self.db.RS_DESTINATION_ID_COLUMN]),
                             data[self.db.RS_DURATION_COLUMN], data[self.db.RS_DISTANCE_COLUMN])
                for data in self.db.get_all_route_segment()]

    @staticmethod
    def _find_pickup_point_by_id(pickup_points, pickup_point_id):
        for pickup_point in pickup_points:
            if pickup_point.get_id() == pickup_point_id:
                return pickup_point
        raise ValueError(f"Pickup point with ID {pickup_point_id} not found")

    def determine_bus_route(self, students, number_of_buses):
        self.students = students
        for _ in range(number_of_buses):
            pass
            # self.buses.append(Bus())

        # 1. Group students by address and dismissal time
        groups = self.group_students(self.students)
        self.print_groups(groups)

        # 2. Create bus routes for students
        self.calculate_bus_route(groups)

    # Group students by dismissal time and address
    @staticmethod
    def group_students(students):
        groups_dict = {}
        for student in students:
            key = (student.address, student.dismissal_time)
            groups_dict.setdefault(key, []).append(student)

        groups_list = list(groups_dict.values())
        return sorted(groups_list, key=lambda group: (group[0].dismissal_time, group[0].address))

    @staticmethod
    def print_groups(groups):
        print("========グループ化された生徒のリスト========")
        for group in groups:
            print(f"{group[0].address} {group[0].dismissal_time}:")
            for student in group:
                print(f"  {student.name}")

    def calculate_bus_route(self, groups):
        # TODO: Implement the bus scheduling algorithm
        pass

    def handle_get_pickup_point(self):

        pass
