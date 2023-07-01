import requests
from Bus import Bus
from Student import Student


class BusRouting:
    def __init__(self):
        self.students = []
        self.buses = []
        self.api_key = "YOUR_API_KEY"

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

    def getTravelTime(self, origin, destination, api_key):
        base_url = "https://maps.googleapis.com/maps/api/directions/json?"

        # パラメータをURLに組み組み込む
        complete_url = f"{base_url}origin={origin}&destination={destination}&key={self.api_key}"

        # APIを呼び出す
        response = requests.get(complete_url)

        # 応答の確認
        response.raise_for_status()

        # 応答からJSONを取得
        directions = response.json()

        # ルートのリストから最初の提案を取得
        route = directions['routes'][0]

        # ルートからレッグのリストを取得し、最初のレッグ（通常は唯一のレッグ）を取得
        leg = route['legs'][0]

        # レッグから所要時間を取得
        duration = leg['duration']

        # 所要時間をリターン
        return duration['text']
