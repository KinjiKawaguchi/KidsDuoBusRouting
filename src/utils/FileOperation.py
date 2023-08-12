import csv
import os
import tkinter as tk
import chardet
from tkinter import filedialog
import bcrypt

from src.api.APIKeyManager import APIKeyManager
from src.api.GoogleMapsClient import GoogleMapsClient
from src.db.PlaceDatabaseManager import PlaceDatabaseManager
from src.db.UserDatabaseManager import UserDatabaseManager
from src.models.Student import Student
from src.models.User import User
from src.utils.ConsoleOperation import ConsoleOperation


class FileOperation:
    env_var_name = "KIDS-DUO_BUS_ROUTING_CRYPTO_KEY"

    def __init__(self):
        self.user_db = UserDatabaseManager('user.db')
        self.place_db = PlaceDatabaseManager('KidsDuoBusRouting.db')
        self.akm = APIKeyManager()
        self.co = ConsoleOperation()
        self.google = None

    def instantiate_google_api_client(self):
        user = self.create_user_instance()
        encrypted_api_key = user.get_encrypted_api_key()
        decrypted_key = self.akm.decrypt_api_key(encrypted_api_key)
        self.google = GoogleMapsClient(decrypted_key)
        return self.google

    """-------------CSVファイル処理-------------"""
    @staticmethod
    def receive_file():
        root = tk.Tk()
        root.withdraw()  # 主要なウィンドウを隠す
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")])  # CSVファイルのみをフィルタリング
        if not file_path:
            print("ファイルが選択されませんでした。")
            return None
        root.destroy()  # Tkのルートウィンドウを破棄
        return file_path

    def read_csv(self, file_path, encoding_type):
        if not self.is_file_right(file_path):
            return None

        try:
            with open(file_path, "r", encoding=encoding_type, errors='replace') as file:
                reader = csv.reader(file)
                return list(reader)
        except Exception as e:
            print(f"Error: CSVファイルの読み込み中にエラーが発生しました: {e}")
            return None
        
    @staticmethod
    def _determine_file_encoding(file_path):
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
        return result['encoding']
        
    @staticmethod
    def is_file_right(file_path):
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

    def instantiate_student(self, file_path):
        rows = self.read_csv(file_path, "utf-8")
        students = []
        for row in rows:
            if len(row) != self.place_db.STUDENT_DATA_COLUMN_NUM:
                print("Error: データが不正です。")
                return None
            name, address, dismissal_time = row
            students.append(Student(name, address, dismissal_time))
        return students
    
    @staticmethod
    def print_registered_data(rows):  # TODO:このメソッドを改修する
        print("登録されたデータは以下の通りです。")
        print("====================================")
        for row in rows:
            print(row[0], row[1])
        
    """-------------ユーザデータ処理-------------"""
    def has_user_records(self):
        if self.user_db.is_table_empty(self.user_db.USERS_TABLE_NAME):
            print("ユーザ情報が登録されていません。")
            return False
        return True

    def get_current_username(self):
        user = self.user_db.get_logged_in_user()
        if not user:
            return None

        if user[self.user_db.USERS_KEEP_LOGGED_IN_COLUMN] == 1:
            username = user[self.user_db.USERS_USERNAME_COLUMN]
            print(f"{username}でログインしています。")
            return username
        return None

    def authenticate(self, username, password):
        if not self.user_db.is_user_exist(username):
            return False
        hashed_password = self.user_db.read_user(username)[self.user_db.USERS_PASSWORD_HASH_COLUMN]
        if hashed_password and self._password_matches(hashed_password, password):
            self.user_db.login(username)
            return True
        return False
    
    def logout(self):
        logout_username = self.get_current_username()
        self.user_db.logout()
        print(f"{logout_username}からログアウトしました。")
        
    def add_user(self, username, hashed_password, encrypted_key, keep_logged_in):
        return self.user_db.create_user(username, hashed_password, encrypted_key, keep_logged_in)

    @staticmethod
    def _password_matches(hashed_password: bytes, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    def create_user_instance(self):
        user_data = self.user_db.get_logged_in_user()
        return User(
            user_data[self.user_db.USERS_ID_COLUMN],
            user_data[self.user_db.USERS_USERNAME_COLUMN],
            user_data[self.user_db.USERS_PASSWORD_HASH_COLUMN],
            user_data[self.user_db.USERS_ENCRYPTED_API_KEY_COLUMN],
            user_data[self.user_db.USERS_KEEP_LOGGED_IN_COLUMN],
            user_data[self.user_db.USERS_IS_LOGGED_IN_COLUMN],
            user_data[self.user_db.USERS_CREATED_AT_COLUMN],
            user_data[self.user_db.USERS_UPDATED_AT_COLUMN]
        )

    """-------------ピックアップポイント処理-------------"""
    def register_pickup_point(self, file_path):
        if self.place_db.is_table_empty("pickup_point"):
            self._handle_empty_pickup_point_table()
        if not self.is_file_right(file_path):
            return None

        encoding = self._determine_file_encoding(file_path)
        rows = self.read_csv(file_path, encoding)
        if rows is None:
            print("Error: データの登録に失敗しました。")
            return None

        return self._process_and_register_pickup_points(rows)

    def get_pickup_point(self, id):
        return self.place_db.get_pickup_point(id)

    def print_all_pickup_point(self):
        pickup_points = self.place_db.get_all_data(self.place_db.PP_TABLE_NAME)
        if not pickup_points:
            print("Error: データベースにデータが存在しません。")
            return None
        print("現在登録されているデータは以下の通りです。")
        print("====================================")
        for pickup_point in pickup_points:
            print(f"ID: {pickup_point[self.place_db.PP_ID_COLUMN]},"
                  f" Name: {pickup_point[self.place_db.PP_NAME_COLUMN]},"
                  f" Address: {pickup_point[self.place_db.PP_ADDRESS_COLUMN]},"
                  f" IsOrigin: {pickup_point[self.place_db.PP_IS_ORIGIN_COLUMN]},"
                  f" CanWait: {pickup_point[self.place_db.PP_CAN_WAIT_COLUMN]}")
        return pickup_points

    # TODO 入力の整合性確認(例:IDが存在するか、名前が空白でないか、など)
    def update_pickup_point(self, id, new_name, new_address, new_can_wait):
        updated_data = self.place_db.update_pickup_point(
            id, new_name, new_address, new_can_wait)
        if updated_data is not None:
            self.update_route_segment(updated_data[self.place_db.PP_ID_COLUMN])

    def delete_pickup_point(self, id):
        deleted_pickup_point = self.place_db.delete_pickup_point(id)
        if deleted_pickup_point is None:
            print("Error: データの削除に失敗しました。")
            return None
        deleted_route_segment_list = self.delete_route_segments(
            deleted_pickup_point[self.place_db.PP_ID_COLUMN])
        self._print_deleted_pickup_point(
            deleted_pickup_point, deleted_route_segment_list)

    def _handle_empty_pickup_point_table(self):
        while True:
            name = self.co.receive_single_str_input("原点となる地点の名前を入力してください: ")
            address = self.co.receive_single_str_input("原点となる地点の住所を入力してください: ")
            print(f"\n入力内容: \n名前: {name} \n住所: {address} ")
            if self.co.receive_yes_or_no_input("この情報でよろしいですか？"):
                self.place_db.add_pickup_point(name, address, True, True)
                break
            else:
                print("再度入力してください。")

    def _process_and_register_pickup_points(self, rows):
        registered_data_list = []
        for row in rows:
            if len(row) != self.place_db.PICKUP_POINT_DATA_COLUMN_NUM:
                print("Error: データが不正です。")
                return None
            name, address, is_origin, can_wait = row
            if self.place_db.is_pickup_point_exists(name=name, address=address):
                print(f"Error: '{name}' , '{address}'はすでにレコードに存在しています。")
            else:
                added_pickup_point = self.place_db.add_pickup_point(name, address, is_origin, can_wait)
                self.register_route_segment(added_pickup_point)
                registered_data_list.append(row)
        return registered_data_list

    def _print_deleted_pickup_point(self, deleted_pickup_point, deleted_route_segment_list):
        print("削除に成功したピックアップポイントのデータは以下の通りです。")
        print("====================================")
        can_wait = True if deleted_pickup_point[self.place_db.PP_CAN_WAIT_COLUMN] == 1 else False
        is_origin = True if deleted_pickup_point[self.place_db.PP_IS_ORIGIN_COLUMN] == 1 else False
        print(f"ID: {deleted_pickup_point[self.place_db.PP_ID_COLUMN]}"
              f" NAME: {deleted_pickup_point[self.place_db.PP_NAME_COLUMN]}"
              f" Address: {deleted_pickup_point[self.place_db.PP_ADDRESS_COLUMN]}"
              f" IsOrigin: {is_origin} CanWait: {can_wait}")
        print("削除に成功したルートセグメントのデータは以下の通りです。")
        print("====================================")
        for deleted_route_segment in deleted_route_segment_list:
            origin_id = deleted_route_segment[self.place_db.RS_ORIGIN_ID_COLUMN]
            destination_id = deleted_route_segment[self.place_db.RS_DESTINATION_ID_COLUMN]
            origin_name, origin_address = self._get_name_and_address(
                origin_id, deleted_pickup_point)
            destination_name, destination_address = self._get_name_and_address(
                destination_id, deleted_pickup_point)

            print(
                f"ID: {deleted_route_segment[self.place_db.RS_ID_COLUMN]}"
                f"{deleted_route_segment[self.place_db.RS_ORIGIN_ID_COLUMN]}"
                f"{origin_name}({origin_address})"
                f"->"
                f"{deleted_route_segment[self.place_db.RS_DESTINATION_ID_COLUMN]}"
                f"{destination_name}({destination_address})"
                f"Duration: {deleted_route_segment[self.place_db.RS_DURATION_COLUMN]}"
                f"Distance: {deleted_route_segment[self.place_db.RS_DISTANCE_COLUMN]})")

    def _get_name_and_address(self, point_id, deleted_pickup_point):
        if point_id == deleted_pickup_point[self.place_db.PP_ID_COLUMN]:
            name = deleted_pickup_point[self.place_db.PP_NAME_COLUMN]
            address = deleted_pickup_point[self.place_db.PP_ADDRESS_COLUMN]
        else:
            pickup_point = self.get_pickup_point(point_id)
            name = pickup_point[self.place_db.PP_NAME_COLUMN]
            address = pickup_point[self.place_db.PP_ADDRESS_COLUMN]
        return name, address
    
    """-------------ルートセグメント処理-------------"""
    def register_route_segment(self, added_pickup_point):
        added_id, added_address = added_pickup_point[
            self.place_db.PP_ID_COLUMN], added_pickup_point[self.place_db.PP_ADDRESS_COLUMN]
        comparing_pickup_point = self.place_db.get_pickup_point(self.place_db.ORIGIN_ID)

        while comparing_pickup_point != added_pickup_point:
            comparison_id = comparing_pickup_point[self.place_db.PP_ID_COLUMN]
            comparing_address = comparing_pickup_point[self.place_db.PP_ADDRESS_COLUMN]

            self._calculate_and_add_route_segment(
                added_id, comparison_id, added_address, comparing_address)

            i = 1
            while not self.place_db.is_pickup_point_exists(id=comparing_pickup_point[self.place_db.PP_ID_COLUMN] + i):
                i += 1
            comparing_pickup_point = self.place_db.get_pickup_point(
                comparing_pickup_point[self.place_db.PP_ID_COLUMN] + i)

    def _calculate_and_add_route_segment(self, origin_id, destination_id, origin_address, destination_address):
        duration, distance = self.google.calculate_duration(
            origin_address, destination_address)
        self.place_db.add_route_segment(
            origin_id, destination_id, duration, distance)

        duration, distance = self.google.calculate_duration(
            destination_address, origin_address)
        self.place_db.add_route_segment(
            destination_id, origin_id, duration, distance)

    def print_all_route_segment(self):
        route_segment_list = self.place_db.get_all_data(self.place_db.RS_TABLE_NAME)
        if not route_segment_list:
            print("Error: データベースにデータが存在しません。")
            return None
        print("登録されたデータは以下の通りです。")
        print("====================================")
        for segment in route_segment_list:
            print(f"ID: {segment[self.place_db.RS_ID_COLUMN]}"
                  f" Origin: {segment[self.place_db.RS_ORIGIN_ID_COLUMN]}"
                  f" Destination: {segment[self.place_db.RS_DESTINATION_ID_COLUMN]}"
                  f" Duration: {segment[self.place_db.RS_DURATION_COLUMN]}"
                  f" Distance: {segment[self.place_db.RS_DISTANCE_COLUMN]}")
        return route_segment_list

    def get_route_segment(self, route_segment_id=None, pickup_point_id=None, origin_id=None, destination_id=None):
        return self.place_db.get_route_segment(route_segment_id, pickup_point_id, origin_id, destination_id)

    def delete_route_segments(self, deleted_pickup_point_id):
        segments_to_delete = self.place_db.get_route_segment(
            pickup_point_id=deleted_pickup_point_id)
        deleted_segments = [segment for segment in segments_to_delete if self.place_db.delete_route_segments(
            route_segment_id=segment[self.place_db.RS_ID_COLUMN])]
        return deleted_segments

    # TODO 入力の整合性を確認する必要がある
    def update_route_segment(self, updated_pickup_point_id=None, route_segment_id=None, new_duration=None,
                             new_distance=None):
        if updated_pickup_point_id:
            self._update_route_segments_by_pickup_point(
                updated_pickup_point_id)
        elif route_segment_id and new_duration and new_distance:
            self._update_specific_route_segment(
                route_segment_id, new_duration, new_distance)
        else:
            print("Error: update_route_segmentの呼び出しエラー")
            return None

    def _update_route_segments_by_pickup_point(self, pickup_point_id):
        segments_to_update = self.get_route_segment(
            pickup_point_id=pickup_point_id)
        for segment in segments_to_update:
            origin_address = self.get_pickup_point(segment[self.place_db.RS_ORIGIN_ID_COLUMN])[
                self.place_db.PP_ADDRESS_COLUMN]
            destination_address = self.get_pickup_point(
                segment[self.place_db.RS_DESTINATION_ID_COLUMN])[self.place_db.PP_ADDRESS_COLUMN]
            duration, distance = self.google.calculate_duration(
                origin_address, destination_address)
            self.update_route_segment(
                route_segment_id=segment[self.place_db.RS_ID_COLUMN], new_duration=duration, new_distance=distance)

    def _update_specific_route_segment(self, route_segment_id, new_duration, new_distance):
        current_segment = self.get_route_segment(route_segment_id)
        updated_segment = self.place_db.update_route_segment(
            route_segment_id, new_duration, new_distance)
        if updated_segment:
            print("更新に成功したデータは以下の通りです。")
            print("====================================")

            current_id, current_origin_id, current_destination_id, current_duration, current_distance = \
                self._extract_segment_data(current_segment)
            dummy_valiable, updated_origin_id, updated_destination_id, updated_duration, updated_distance = \
                self._extract_segment_data(updated_segment)

            # 結果を整形して出力
            print("Segment Data:")
            print(f"ID:           {current_id}")
            print(
                f"Origin:       {self._display_with_arrows(current_origin_id, updated_origin_id)}")
            print(
                f"Destination:  {self._display_with_arrows(current_destination_id, updated_destination_id)}")
            print(
                f"Duration:     {self._display_with_arrows(current_duration, updated_duration)}")
            print(
                f"Distance:     {self._display_with_arrows(current_distance, updated_distance)}")

            return updated_segment
        else:
            print("更新に失敗しました。")
            return None

    def _extract_segment_data(self, segment):
        segment_id = segment[self.place_db.RS_ID_COLUMN]
        origin_id = segment[self.place_db.RS_ORIGIN_ID_COLUMN]
        destination_id = segment[self.place_db.RS_DESTINATION_ID_COLUMN]
        duration = segment[self.place_db.RS_DURATION_COLUMN]
        distance = segment[self.place_db.RS_DISTANCE_COLUMN]
        return segment_id, origin_id, destination_id, duration, distance

    """-------------共通処理-------------"""
    @staticmethod
    def _display_with_arrows(current_data, updated_data):
        arrow = "→" if current_data != updated_data else ""
        return f"{current_data:<20} {arrow:<3} {updated_data}"
