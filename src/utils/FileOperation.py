import csv
import os
import tkinter as tk

from tkinterdnd2 import DND_FILES, TkinterDnD

from src.api.GoogleMapsClient import GoogleMapsClient
from src.db.DatabaseManager import DatabaseManager
from src.models.Student import Student


class FileOperation:
    API_KEY = ""

    def __init__(self):
        self.file_path = ''
        self.root = TkinterDnD.Tk()

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
        self.root.withdraw()
        self.setup_ui()  # GUIの構成部分をここで呼び出す
        self.root.deiconify()
        self.root.mainloop()

        return self.file_path

    def read_csv(self, file_path, encoding_type):
        print(f"ファイルパス: {file_path}")
        if not os.path.exists(file_path):
            print("Error: ファイルが存在しません")
            return None

        if not os.path.isfile(file_path):
            print("Error: ファイルパスが無効です")
            return None

        if not file_path.endswith(".csv"):
            print("Error: CSVファイルではありません")
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

    def register_pick_up_point(self, file_path):
        # Use your actual database name
        db = DatabaseManager('KidsDuoBusRouting.db')

        # データベースが空の場合はユーザーに原点となる地点を入力してもらう
        if db.is_table_empty():
            while True:
                name = input('原点となる地点の名前を入力してください: ')
                address = input('原点となる地点の住所を入力してください: ')

                # ユーザーに入力を確認してもらう
                print(f"\n入力内容: \n名前: {name} \n住所: {address}")
                while True:
                    is_confirm = input("この情報でよろしいですか？ (yes/no): ").lower()
                    if is_confirm == "yes" or is_confirm == "no":
                        break
                if is_confirm == "yes":
                    added_pickup_point = db.add_pickup_point(name, address)
                    if added_pickup_point != None:
                        pass
                    break
                else:
                    print("再度入力してください。")

        rows = self.read_csv(file_path, "utf-8")

        for row in rows:
            if len(row) != 2:
                print("Error: データが不正です。")
                return None

        registered_datas = []
        for row in rows:
            name, address = row
            if db.is_pickup_point_exits(name):
                print(f"Error: '{name}' already exists in the database.")
            else:
                added_pickup_point = db.add_pickup_point(name, address)
                for added_pickup_point in added_pickup_point:
                    db.add_route_segment()
                if added_pickup_point != None:
                    pass
                registered_datas.append(row)

        return registered_datas

    def print_registeredData(self, rows):
        print("登録されたデータは以下の通りです。")
        print("====================================")
        for row in rows:
            print(row[0], row[1])

    def print_all_pickup_point(self):
        db = DatabaseManager('KidsDuoBusRouting.db')
        places = db.get_all_pickup_points()
        for place in places:
            print(f"ID: {place[0]}, Name: {place[1]}, Address: {place[2]}")

    def update_pickup_point(self, id, new_name, new_address):
        db = DatabaseManager('KidsDuoBusRouting.db')
        updated_data = db.update_pickup_point(id, new_name, new_address)
        if updated_data != None:
            pass

    def delete_pickup_point(self, id):
        db = DatabaseManager('KidsDuoBusRouting.db')
        deleted_data = db.delete_pickup_point(id)
        if deleted_data != None:
            pass

    def add_route_segment(self, added_pickup_point):
        google = GoogleMapsClient()
        db = DatabaseManager('KidsDuoBusRouting.db')

        added_id = added_pickup_point[0]
        added_address = added_pickup_point[2]

        db.get_route_segment(0)
        comparing_pickup_point = self.cursor.fetchone()

        while comparing_pickup_point != added_pickup_point:
            comparisonId = comparing_pickup_point[0]
            comparing_address = comparing_pickup_point[2]

            duration, distance = google.calculate_duration(
                added_address, comparing_address)
            db.add_route_segment(added_id, comparisonId, duration, distance)

            duration, distance = google.calculate_duration(
                comparing_address, added_address)
            db.add_route_segment(comparisonId, added_id, duration, distance)

            i = 1
            while not (self.is_pickup_point_exits(comparing_pickup_point[0] + 1)):
                i += 1
            db.get_route_segment(comparing_pickup_point[0] + i)
            comparing_pickup_point = self.cursor.fetchone()
        self.conn.commit()
