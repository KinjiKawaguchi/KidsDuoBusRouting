from Bus import Bus


class BusRouting:
    def __init__(self):
        self.students = []
        self.buses = []

    def executeBusRouting(self, students, numberOfBuses):
        self.students = students
        for i in range(numberOfBuses):
            self.buses.append(Bus())

        # 1. 生徒を住所と下校時間でグループ化する
        groups = self.groupStudentsByAttribute(self.students)
        self.printGroups(groups)

        # 2. 生徒をバスに乗せるルートを作成
        self.createBusRoutes(groups)

    # 生徒を下校時間と小学校でグループ化
    def groupStudentsByAttribute(self, students):
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

    def printGroups(self, groups):
        print("========グループ化された生徒のリスト========")
        for group in groups:
            print(f"{group[0].address} {group[0].dismissal_time}:")
            for student in group:
                print(f"  {student.name}")

    def createBusRoutes(self, groups):
        # バス配車アルゴリズムをコーディング
        pass