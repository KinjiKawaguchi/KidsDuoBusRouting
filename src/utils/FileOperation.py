import csv
import os
import tkinter as tk
import chardet

from tkinterdnd2 import DND_FILES, TkinterDnD

from src.api.GoogleMapsClient import GoogleMapsClient
from src.db.DatabaseManager import DatabaseManager
from src.models.Student import Student


class FileOperation:
    API_KEY = ""

    def __init__(self):
        self.file_path = ''
        self.db = DatabaseManager('KidsDuoBusRouting.db')

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
            with open(file_path, "r", encoding=encoding_type) as file:
                reader = csv.reader(file)
                return list(reader)
        except Exception as e:
            print(f"Error: CSVファイルの読み込み中にエラーが発生しました: {e}")
            return None

    def instantiate_student(self, filePath):
        rows = self.read_csv(filePath, "utf-8")

        students = []

        for row in rows:
            if len(row) != 3:
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

    for row in rows:
        if len(row) != 4:
            print("Error: データが不正です。")
            return None

    registered_datas = []
    for row in rows:
        name, address, is_origin, can_wait = row
        if self.db.is_pickup_point_exits(name, address):
            print(f"Error: '{name}' already exists in the database.")
        else:
            added_pickup_point = self.db.add_pickup_point(
                name, address, is_origin, can_wait)
            for added_pickup_point in added_pickup_point:
                self.db.add_route_segment()
            registered_datas.append(row)

    return registered_datas

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
                f"ID: {pickup_point[0]}, Name: {pickup_point[1]}, Address: {pickup_point[2]}, IsOrigin: {pickup_point[3]}, CanWait: {pickup_point[4]}")
        return pickup_points

    def update_pickup_point(self, id, new_name, new_address, new_can_wait):

        updated_data = self.db.update_pickup_point(
            id, new_name, new_address, new_can_wait)
        if updated_data != None:
            pass

    def delete_pickup_point(self, id):

        deleted_datas = self.db.delete_pickup_point(id)
        if deleted_datas == []:
            print("Error: データの削除に失敗しました。")
            return None
        print("削除に成功したデータは以下の通りです。")
        print("====================================")
        for deleted_data in deleted_datas:
            print("ID: ", deleted_data[0], "Name: ", deleted_data[1]),"Address: ", deleted_data[2], "IsOrigin: ", deleted_data[3], "CanWait: ", deleted_data[4]
            deleted_data_id = deleted_data[0]
            related_route_segments = self.db.get_related_route_segments(deleted_data_id)
            for related_route_segment in related_route_segments:
                deleted_route_segment = self.db.delete_route_segment(related_route_segment[0])
                print("ID: ", deleted_route_segment[0], "Origin: ", deleted_route_segment[1], "Destination: ", deleted_route_segment[2], "Duration: ", deleted_route_segment[3], "Distance: ", deleted_route_segment[4])
                
        
            

    def add_route_segment(self, added_pickup_point):
        google = GoogleMapsClient()

        added_id = added_pickup_point[0]
        added_address = added_pickup_point[2]

        self.db.get_route_segment(0)
        comparing_pickup_point = self.cursor.fetchone()

        while comparing_pickup_point != added_pickup_point:
            comparisonId = comparing_pickup_point[0]
            comparing_address = comparing_pickup_point[2]

            duration, distance = google.calculate_duration(
                added_address, comparing_address)
            self.db.add_route_segment(
                added_id, comparisonId, duration, distance)

            duration, distance = google.calculate_duration(
                comparing_address, added_address)
            self.db.add_route_segment(
                comparisonId, added_id, duration, distance)

            i = 1
            while not (self.is_pickup_point_exits(comparing_pickup_point[0] + 1)):
                i += 1
            self.db.get_route_segment(comparing_pickup_point[0] + i)
            comparing_pickup_point = self.cursor.fetchone()
        self.conn.commit()

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

    def update_route_segment(self, id, new_duration, new_distance):
        updated_data = self.db.update_route_segment(
            id, new_duration, new_distance)
        if updated_data != []:
            print("更新に成功したデータは以下の通りです。")
            print("====================================")
            print(
                f"ID: {updated_data[0]}, Origin: {updated_data[1]}, Destination: {updated_data[2]}, Duration: {updated_data[3]}, Distance: {updated_data[4]}")
            return updated_data
        print("更新に失敗しました。")
        return None
