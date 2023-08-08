from src.models.Bus import Bus
from src.models.Student import Student
from src.models.PickupPoint import PickupPoint
from src.models.RouteSegment import RouteSegment

from src.db.DatabaseManager import DatabaseManager
from src.utils.FileOperation import FileOperation


class BusRouting:
    def __init__(self):
        self.load_data()

    def load_data(self):
        db = DatabaseManager("KidsDuoBusRouting.db")

        # ピックアップポイントのインスタンス化
        pickup_point_list = self._instantiate_pickup_points(db)

        # ルートセグメントのインスタンス化
        route_segment_list = self._instantiate_route_segments(db, pickup_point_list)

    def _instantiate_pickup_points(self, db):
        pickup_point_list = []
        data_tmp = db.get_all_pickup_points()
        for data in data_tmp:
            pickup_point_list.append(PickupPoint(data[db.PP_ID_COLUMN], data[db.PP_NAME_COLUMN],
                                                data[db.PP_ADDRESS_COLUMN], data[db.PP_IS_ORIGIN_COLUMN], data[db.PP_CAN_WAIT_COLUMN]))
        return pickup_point_list

    def _instantiate_route_segments(self, db, pickup_point_list):
        route_segment_list = []
        data_tmp = db.get_all_route_segments()
        for data in data_tmp:
            origin_pickup_point = self._find_pickup_point_by_id(pickup_point_list, data[db.RS_ORIGIN_ID_COLUMN])
            destination_pickup_point = self._find_pickup_point_by_id(pickup_point_list, data[db.RS_DESTINATION_ID_COLUMN])
            route_segment_list.append(RouteSegment(
                data[db.RS_ID_COLUMN], origin_pickup_point, destination_pickup_point, data[db.RS_DURATION_COLUMN], data[db.RS_DISTANCE_COLUMN]))
        return route_segment_list

    def _find_pickup_point_by_id(self, pickup_point_list, pickup_point_id):
        for pickup_point in pickup_point_list:
            if pickup_point.get_id() == pickup_point_id:
                return pickup_point
        raise ValueError(f"Pickup point with ID {pickup_point_id} not found")

    def determining_bus_route(self, students, bus_count):
        self.students = students
        for i in range(bus_count):
            self.buses.append(Bus())

        # 1. 生徒を住所と下校時間でグループ化する
        groups = self.grouping_students(self.students)
        self.print_groups(groups)

        # 2. 生徒をバスに乗せるルートを作成
        self.calculate_bus_route(groups)

    # 生徒を下校時間と小学校でグループ化
    def grouping_student(self, students):
        # { (address, dismissal_time): [student1, student2, ...], ... }
        groups_dict = {}
        for student in students:
            key = (student.address, student.address, student.dismissal_time)
            if key in groups_dict:
                groups_dict[key].append(student)
            else:
                groups_dict[key] = [student]

        # Convert dictionary to list and sort by dismissal time and school name
        groups_list = list(groups_dict.values())
        sorted_groups = sorted(groups_list, key=lambda group: (
            group[0].dismissal_time, group[0].address))

        return sorted_groups

    def print_groups(self, groups):
        print("========グループ化された生徒のリスト========")
        for group in groups:
            print(f"{group[0].address} {group[0].dismissal_time}:")
            for student in group:
                print(f"  {student.name}")

    def calculate_bus_route(self, groups):
        # バス配車アルゴリズムをコーディング
        pass
