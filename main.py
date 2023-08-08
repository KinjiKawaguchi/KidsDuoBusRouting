import sys
import os

# from PyQt5.QtWidgets import QApplication

from src.services.BusRouting import BusRouting
# from src.view.MainWindow import MainWindow

from src.utils.ConsoleOperation import ConsoleOperation
from src.utils.FileOperation import FileOperation

if __name__ == "__main__":
    co = ConsoleOperation()
    while True:
        print("====================================")
        print("KidsDuoバスルーティングシステム")
        print("====================================")
        options = ["バスの経路を計算", "ピックアップポイントのデータ管理", "ルートセグメントのデータ管理", "終了"]
        action = co.receive_input(options)

        fo = FileOperation()

        if action == 1:
            # バスの経路を計算
            # ドラッグアンドドロップでファイルパスを取得
            file_path = fo.receive_file()
            students = fo.instantiate_student(file_path)

            br = BusRouting()
            br.determining_bus_route(students, NUMBER_OF_BUSES)

        elif action == 2:
            options = ["登録", "表示", "更新", "削除", "終了"]
            crud_action = co.receive_input(options)
            if crud_action == 1:  # Create
                options = ["ファイルから入力", "キーボードで入力", "終了"]
                input_way = co.receive_input(options)
                if input_way == 1:
                    file_path = fo.receive_file()
                    registered_data = fo.register_pickup_point(file_path)
                    if registered_data is not None:
                        fo.print_registeredData(registered_data)
                    else:
                        print("Error: データの登録に失敗しました。")
                elif input_way == 2:
                    """
                    new_name = co.receive_single_str_input("新しい名前を入力してください: ")
                    new_address = co.receive_single_str_input(
                        "新しい住所を入力してください: ")
                    new_is_origin = co.receive_single_str_input(
                        "教室データですか？ (yes/no): ").lower()
                    new_can_wait = co.receive_single_str_input(
                        "待機可能ですか？ (yes/no): ").lower()
                    """
                    print("キーボードからの入力は現在未実装です。")
                    pass

                elif input_way == 3:
                    print("終了します。")
                    sys.exit()
            elif crud_action == 2:  # Read
                fo.print_all_pickup_point()
            elif crud_action == 3:  # Update
                pickup_points = fo.print_all_pickup_point()
                if pickup_points is not None:
                    pickup_point_id_list = co.receive_multiple_str_input(
                        "更新したいデータのIDを入力してください: ")
                    for pickup_point_id in pickup_point_id_list:
                        current_name = fo.get_pickup_point(pickup_point_id)[1]
                        current_address = fo.get_pickup_point(pickup_point_id)[2]
                        current_is_origin = fo.get_pickup_point(pickup_point_id)[3]
                        current_can_wait = fo.get_pickup_point(pickup_point_id)[4]

                        print(
                            f"ID {pickup_point_id} \n名前: {current_name}\n住所: {current_address} \n教室データ:{current_is_origin}\n待てる場所か:{current_can_wait}")

                        new_name = co.receive_single_str_input(
                            f"ID {pickup_point_id} の新しい名前を入力してください: ")
                        new_address = co.receive_single_str_input(
                            f"ID {pickup_point_id} の新しい住所を入力してください:")
                        new_can_wait = co.receive_single_str_input(
                            f"ID {pickup_point_id} の待てる場所かを入力してください: ")
                        fo.update_pickup_point(
                            pickup_point_id, new_name, new_address, new_can_wait)
            elif crud_action == 4:  # Delete
                pickup_points = fo.print_all_pickup_point()
                if pickup_points is not None:
                    pickup_point_id_list = co.receive_multiple_str_input(
                        "削除したいデータのIDを入力してください:  ")
                    for pickup_point_id in pickup_point_id_list:
                        fo.delete_pickup_point(pickup_point_id)
            elif crud_action == 5:  # Exit
                print("終了します。")
                sys.exit()
        elif action == 3:
            options = ["表示", "更新", "終了"]
            crud_action = co.receive_input(options)
            if crud_action == 1:
                fo.print_all_route_segment()
            elif crud_action == 2:
                route_segments = fo.print_all_route_segment()
                if route_segments is not None:
                    pickup_point_id_list = co.receive_multiple_str_input(
                        "更新するデータのIDを入力してください。(複数可):")
                    for pickup_point_id in pickup_point_id_list:
                        origin_name = fo.get_pickup_point(
                            fo.get_route_segment(pickup_point_id)[5])[1]
                        destination_name = fo.get_pickup_point(
                            fo.get_route_segment(pickup_point_id)[6])[1]
                        current_duration = fo.get_route_segment(pickup_point_id)[3]
                        current_distance = fo.get_route_segment(pickup_point_id)[4]

                        print(
                            f"ID {pickup_point_id} の出発地点は {origin_name}で、到着地点は{destination_name} です。")
                        print(
                            f"現在登録されている所要時間は {current_duration}分で、現在登録されている距離は{current_distance} km です。")

                        new_duration = co.receive_single_str_input(
                            f"ID {pickup_point_id}に対して新しく登録する所要時間を入力: ")
                        new_distance = co.receive_single_str_input(
                            f"ID {pickup_point_id}に対して新しく登録する距離を入力: ")

                        fo.update_route_segment(pickup_point_id, new_duration, new_distance)
            elif crud_action == 3:
                print("終了します。")
                sys.exit()
        elif action == 4:  # Exit
            print("終了します。")
            sys.exit()
