import csv
import os
import tkinter as tk
import chardet

from tkinterdnd2 import DND_FILES, TkinterDnD

from src.api.GoogleMapsClient import GoogleMapsClient
from src.db.DatabaseManager import DatabaseManager
from src.models.Student import Student


class FileOperation:
    def __init__(self):
        self.file_path = ''
        self.db = DatabaseManager('KidsDuoBusRouting.db')
        self.google = GoogleMapsClient()

    def drop(self, event):
        self.file_path = event.data
        self.root.quit()

    def setup_ui(self):  # GUIの構成を行う新たなメソッドを作成
        self.frame = tk.Frame(self.root, name='drag-drop-area', width=400,
                              height=400)  # Initialize the frame in the constructor
        self.frame.pack()
        self.root.update()
        self.root.dnd_accept = lambda x: x
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.frame.drop_target_register(DND_FILES)
        self.frame.dnd_bind('<<Drop>>', self.drop)

    def receive_file(self):
        self.root = TkinterDnD.Tk()
        self.root.withdraw()
        self.setup_ui()  # GUIの構成部分をここで呼び出す
        self.root.deiconify()
        self.root.mainloop()

        return self.file_path

    def read_csv(self, file_path, encoding_type):
        if not (self.is_file_right(file_path)):
            return None

        try:
            with open(file_path, "r", encoding=encoding_type, errors='replace') as file:
                reader = csv.reader(file)
                return list(reader)
        except Exception as e:
            print(f"Error: CSVファイルの読み込み中にエラーが発生しました: {e}")
            return None

    def instantiate_student(self, filePath):
        rows = self.read_csv(filePath, "utf-8")

        students = []

        for row in rows:
            if len(row) != self.db.STUDENT_DATA_ROW_COLUMN:
                print("Error: データが不正です。")
                return None

            name = row[0]
            address = row[1]
            dismissal_time = row[2]

            student = Student(name, address, dismissal_time)
            students.append(student)

        return students

    def register_pickup_point(self, file_path):
        # Use your actual database name
        # データベースが空の場合はユーザーに原点となる地点を入力してもらう
        if self.db.is_table_empty():
            while True:
                name = input('原点となる地点の名前を入力してください: ')
                address = input('原点となる地点の住所を入力してください: ')

                # ユーザーに入力を確認してもらう
                print(
                    f"\n入力内容: \n名前: {name} \n住所: {address} ")
                while True:
                    is_confirm = input("この情報でよろしいですか？ (yes/no): ").lower()
                    if is_confirm == "yes" or is_confirm == "no":
                        break
                if is_confirm == "yes":
                    self.db.add_pickup_point(name, address, True, True)
                    break
                else:
                    print("再度入力してください。")

        if not (self.is_file_right(file_path)):
            return None

        # Determine the file encoding
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())

        encoding = result['encoding']

        rows = self.read_csv(file_path, encoding)
        if rows is None:
            print("Error: データの登録に失敗しました。")
            return None

        for row in rows:
            if len(row) != self.db.PICKUP_POINT_DATA_ROW_COLUMN:
                print("Error: データが不正です。")
                return None

        registered_data_list = []
        for row in rows:
            name, address, is_origin, can_wait = row
            if self.db.is_pickup_point_exists(name=name, address=address):
                print(f"Error: '{name}' , '{address}'はすでにレコードに存在しています。")
            else:
                added_pickup_point = self.db.add_pickup_point(
                    name, address, is_origin, can_wait)
                self.register_route_segment(added_pickup_point)
                registered_data_list.append(row)

        return registered_data_list

    def is_file_right(self, file_path):
        if not os.path.exists(file_path):
            print("Error: ファイルが存在しません")
            return False

        if not os.path.isfile(file_path):
            print("Error: ファイルパスが無効です")
            return False

        if not file_path.endswith(".csv"):
            print("Error: CSVファイルではありません")
            return False
        return True

    def print_registeredData(self, rows):
        print("登録されたデータは以下の通りです。")
        print("====================================")
        for row in rows:
            print(row[0], row[1])
            # TODO: ここの処理をピックアップポイント以外のデータも表示できる汎用性を持たせる

    def get_pickup_point(self, id):
        pickup_point = self.db.get_pickup_point(id)
        if pickup_point != None:
            return pickup_point
        return None

    def print_all_pickup_point(self):
        pickup_points = self.db.get_all_pickup_points()
        if pickup_points == []:
            print("Error: データベースにデータが存在しません。")
            return None
        print("現在登録されているデータは以下の通りです。")
        print("====================================")
        for pickup_point in pickup_points:
            print(
                f"ID: {pickup_point[self.db.PP_ID_COLUMN]}, Name: {pickup_point[self.db.PP_NAME_COLUMN]}, Address: {pickup_point[self.db.PP_ADDRESS_COLUMN]}, IsOrigin: {pickup_point[self.db.PP_IS_ORIGIN_COLUMN]}, CanWait: {pickup_point[self.db.PP_CAN_WAIT_COLUMN]}")
        return pickup_points

    def update_pickup_point(self, id, new_name, new_address, new_can_wait):

        updated_data = self.db.update_pickup_point(
            id, new_name, new_address, new_can_wait)
        if updated_data != None:
            pass

    def delete_pickup_point(self, id):
        deleted_pickup_point_list = self.db.delete_pickup_point(id)
        if deleted_pickup_point_list is None:
            print("Error: データの削除に失敗しました。")
            return None
        deleted_route_segment_list = None
        for deleted_pickup_point in deleted_pickup_point_list:
            deleted_route_segment_list.append(
                self.delete_route_segment(deleted_pickup_point[0]))

        print("削除に成功したピックアップポイントのデータは以下の通りです。")
        print("====================================")
        for deleted_pickup_point in deleted_pickup_point_list:
            can_wait = True if deleted_pickup_point[self.db.PP_CAN_WAIT_COLUMN] == 1 else False
            is_origin = True if deleted_pickup_point[self.db.PP_IS_ORIGIN_COLUMN] == 1 else False
            print(
                f"ID: {deleted_pickup_point[self.db.PP_ID_COLUMN]} NAME: {deleted_pickup_point[self.db.PP_NAME_COLUMN]} Address: {deleted_pickup_point[self.db.PP_ADDRESS_COLUMN]} IsOrigin: {is_origin} CanWait: {can_wait}")
        print("削除に成功したルートセグメントのデータは以下の通りです。")
        print("====================================")
        for deleted_route_segment in deleted_route_segment_list:
            origin_pickup_point = self.db.get_pickup_point(
                deleted_route_segment[self.db.RS_ORIGIN_ID_COLUMN])
            origin_name = origin_pickup_point[self.db.PP_NAME_COLUMN]
            origin_address = origin_pickup_point[self.db.PP_ADDRESS_COLUMN]
            destination_pickup_point = self.db.get_pickup_point[
                deleted_route_segment[self.db.RS_DESTINATION_ID_COLUMN]]
            destination_name = destination_pickup_point[self.db.PP_NAME_COLUMN]
            destination_address = destination_pickup_point[self.db.PP_ADDRESS_COLUMN]
            print(f"ID: {deleted_route_segment[self.db.RS_ID_COLUMN]} OriginName: {origin_name} OriginAddress: {origin_address} DestionationName: {destination_name} DestionationAddress: {destination_address} Duration: {deleted_route_segment[self.db.RS_DURATION_COLUMN]} Distance: {deleted_route_segment[self.db.RS_DISTANCE_COLUMN]}")

    def register_route_segment(self, added_pickup_point):

        added_id = added_pickup_point[0]
        added_address = added_pickup_point[2]

        comparing_pickup_point = self.db.get_pickup_point(
            self.db.ORIGIN_ID)

        while comparing_pickup_point != added_pickup_point:
            comparisonId = comparing_pickup_point[0]
            comparing_address = comparing_pickup_point[2]

            duration, distance = self.google.calculate_duration(
                added_address, comparing_address)
            self.db.add_route_segment(
                added_id, comparisonId, duration, distance)

            duration, distance = self.google.calculate_duration(
                comparing_address, added_address)
            self.db.add_route_segment(
                comparisonId, added_id, duration, distance)

            i = 1
            while not (self.db.is_pickup_point_exists(id=comparing_pickup_point[0] + i)):
                i += 1
            comparing_pickup_point = self.db.get_pickup_point(
                comparing_pickup_point[0] + i)

    def print_all_route_segment(self):
        route_segments = self.db.get_all_route_segments()
        if route_segments == []:
            print("Error: データベースにデータが存在しません。")
            return None
        print("登録されたデータは以下の通りです。")
        print("====================================")
        for route_segment in route_segments:
            print(
                f"ID: {route_segment[0]}, Origin: {route_segment[1]}, Destination: {route_segment[2]}, Duration: {route_segment[3]}, Distance: {route_segment[4]}")
        return route_segments

    def get_route_segment(self, id):
        route_segment = self.db.get_route_segment(id)
        if route_segment == []:
            return None
        return route_segment

        # 削除はピックアップポイントが削除された時のみ実行される
    def delete_route_segment(self, deleted_pickup_point_id):
        delete_route_segment_list = self.db.get_route_segment(
            pickup_point_id=deleted_pickup_point_id)
        deleted_route_segment_list = None
        for delete_route_segment in delete_route_segment_list:
            deleted_route_segment = self.db.delete_route_segment(
                delete_route_segment[0])
            if deleted_route_segment is not None:
                deleted_route_segment_list.append(delete_route_segment)
        return deleted_route_segment_list

    # 更新はピックアップポイントのデータ更新のタイミング、またはユーザがルートセグメントの情報を編集する場合に行われる
    def update_route_segment(self, updated_pickup_point_id=None, route_segment_id=None, new_duration=None, new_distance=None):
        if route_segment_id and new_duration and new_distance is not None:
            current_route_segment = self.db.get_route_segment(
                route_segment_id=route_segment_id)
            updated_route_segment = self.db.update_route_segment(
                route_segment_id, new_duration, new_distance)
            if updated_route_segment != []:
                print("更新に成功したデータは以下の通りです。")
                print("====================================")

                print(
                    f"ID: {updated_route_segment[0]}, Origin: {updated_route_segment[1]}, Destination: {updated_route_segment[2]}, Duration: {updated_route_segment[3]}, Distance: {updated_route_segment[4]}")
                return updated_route_segment
            print("更新に失敗しました。")
            return None
        elif updated_pickup_point_id is not None:
            update_route_segment_list = self.get_route_segmnet(
                pickup_point_id=updated_pickup_point_id)
            for update_route_segment in update_route_segment_list:
                origin_id = update_route_segment[self.db.RS_ORIGIN_ID_COLUMN]
                destination_id = update_route_segment[self.db.RS_DESTINATION_ID_COLUMN]
                origin_address = self.get_pickup_point(
                    origin_id)[self.db.PP_ADDRESS_COLUMN]
                destination_address = self.get_pickup_point(
                    destination_id)[self.db.PP_ADDRESS_COLUMN]
                calculated_duration, calculated_distance = self.google.calculate_duration(
                    origin_address, destination_address)
                self.update_route_segment(
                    route_segment_id=update_route_segment[self.db.RS_ID_COLUMN], new_duration=calculated_duration, new_distance=calculated_distance)
        else:
            print("Error: update_route_segmentの呼び出しエラー")
            return None
