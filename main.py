import sys

from PyQt5.QtWidgets import QApplication
from src.view.MainWindow import MainWindow

from src.utils.ConsoleOperation import ConsoleOperation

NUMBER_OF_BUSES = 3

if __name__ == "__main__":
    co = ConsoleOperation()
    while True:
        print("====================================")
        print("KidsDuoバスルーティングシステム")
        print("====================================")
        options = ["バスの経路を計算", "ピックアップポイントのデータ管理", "終了"]
        action = co.receive_input(options)

        # ファイル管理のためクラスインスタンスを作成
        fo = FileOperation()

        if action == 0:
            # バスの経路を計算

            # ドラッグアンドドロップでファイルパスを取得
            filePath = fo.receive_file()
            students = fo.instantiate_student(filePath)

            br = BusRouting()
            br.determining_bus_route(students, NUMBER_OF_BUSES)

        elif action == 1:
            # ピックアップポイントのデータ管理
            options = ["登録", "表示", "更新", "削除", "終了"]
            crud_action = co.receive_input(options)

            if crud_action == 0:  # Create
                # ドラッグアンドドロップでファイルパスを取得
                options = ["ファイルから入力", "キーボードで入力"]
                wayToInput = co.receive_input(options)
                if wayToInput == 0:
                    filePath = fo.receive_file()
                    registeredData = fo.register_pick_up_point(filePath)
                    if registeredData is not None:
                        
                        fo.print_registeredData(registeredData)
                    else:
                        print("Error: データの登録に失敗しました。")
                elif wayToInput == 1:
                    new_name = co.receive_single_str_input("新しい名前を入力してください: ")
                    new_address = co.receive_single_str_input("新しい住所を入力してください: ")
                    pass

            elif crud_action == 1:  # Read
                fo.print_all_pickup_point()

            elif crud_action == 2:  # Update
                db = DatabaseManager('KidsDuoBusRouting.db')
                fo.print_all_pickup_point()
                id_list = co.receive_multiple_str_input("更新したいデータのIDを入力してください: ")

                for id in id_list:
                    current_name = db.get_pickup_point(id)[1]
                    current_address = db.get_pickup_point(id)[2]

                    print(f"ID {id} の現在の名前は {current_name} で、現在の住所は {current_address} です。")

                    new_name = co.receive_single_str_input(f"ID {id} の新しい名前を入力してください: ")
                    new_address = co.receive_single_str_input(f"ID {id} の新しい住所を入力してください: ")
                    fo.update_pickup_point(id, new_name, new_address)



            elif crud_action == 3:  # Delete
                fo.print_all_pickup_point()
                id_list = co.receive_multiple_str_input("削除したいデータのIDを入力してください: ")
                for id in id_list:
                    fo.delete_pickup_point(id)

            elif crud_action == 4:  # Exit
                print("終了します。")
                break
        elif action == 2:  # Exit
            print("終了します。")
            break
