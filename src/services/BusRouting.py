from src.models.Bus import Bus
from src.models.Student import Student
from src.models.PickupPoint import PickupPoint
from src.models.RouteSegment import RouteSegment

from src.db.DatabaseManager import DatabaseManager
from src.utils.FileOperation import FileOperation


class BusRouting:
    def __init__(self):
        self.buses = []
        self.load_data()

    def load_data(self):
        db = DatabaseManager("KidsDuoBusRouting.db")

        # Instantiate pickup points
        self.pickup_points = self._instantiate_pickup_points(db)

        # Instantiate route segments
        self.route_segments = self._instantiate_route_segments(db, self.pickup_points)

    def _instantiate_pickup_points(self, db):
        return [PickupPoint(data[db.PP_ID_COLUMN], data[db.PP_NAME_COLUMN],
                            data[db.PP_ADDRESS_COLUMN], data[db.PP_IS_ORIGIN_COLUMN], data[db.PP_CAN_WAIT_COLUMN])
                for data in db.get_all_pickup_points()]

    def _instantiate_route_segments(self, db, pickup_points):
        return [RouteSegment(data[db.RS_ID_COLUMN],
                             self._find_pickup_point_by_id(pickup_points, data[db.RS_ORIGIN_ID_COLUMN]),
                             self._find_pickup_point_by_id(pickup_points, data[db.RS_DESTINATION_ID_COLUMN]),
                             data[db.RS_DURATION_COLUMN], data[db.RS_DISTANCE_COLUMN])
                for data in db.get_all_route_segments()]

    def _find_pickup_point_by_id(self, pickup_points, pickup_point_id):
        for pickup_point in pickup_points:
            if pickup_point.get_id() == pickup_point_id:
                return pickup_point
        raise ValueError(f"Pickup point with ID {pickup_point_id} not found")

    def determine_bus_route(self, students, bus_count):
        self.students = students
        for _ in range(bus_count):
            self.buses.append(Bus())

        # 1. Group students by address and dismissal time
        groups = self.group_students(self.students)
        self.print_groups(groups)

        # 2. Create bus routes for students
        self.calculate_bus_route(groups)

    # Group students by dismissal time and address
    def group_students(self, students):
        groups_dict = {}
        for student in students:
            key = (student.address, student.dismissal_time)
            groups_dict.setdefault(key, []).append(student)

        groups_list = list(groups_dict.values())
        return sorted(groups_list, key=lambda group: (group[0].dismissal_time, group[0].address))

    def print_groups(self, groups):
        print("========グループ化された生徒のリスト========")
        for group in groups:
            print(f"{group[0].address} {group[0].dismissal_time}:")
            for student in group:
                print(f"  {student.name}")

    def calculate_bus_route(self, groups):
        # TODO: Implement the bus scheduling algorithm
        pass
