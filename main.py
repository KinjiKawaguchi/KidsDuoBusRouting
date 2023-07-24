from BusRouting import BusRouting
from ConsoleOperation import ConsoleOperation
from DatabaseManager import DatabaseManager
from FileOperation import FileOperation

NUMBER_OF_BUSES = 3

if __name__ == "__main__":
    co = ConsoleOperation()
    while True:
        print("====================================")
        print("KidsDuoバスルーティングシステム")
        print("====================================")
        options = ["バスの経路を計算", "ピックアップポイントのデータ管理", "終了"]
        action = co.getInput(options)

        # ファイル管理のためクラスインスタンスを作成
        fo = FileOperation()

        if action == 0:
            # バスの経路を計算

            # ドラッグアンドドロップでファイルパスを取得
            filePath = fo.inputFile()
            students = fo.setStudentData(filePath)

            br = BusRouting()
            br.executeBusRouting(students, NUMBER_OF_BUSES)

        elif action == 1:
            # ピックアップポイントのデータ管理
            options = ["登録", "表示", "更新", "削除", "終了"]
            crud_action = co.getInput(options)

            if crud_action == 0:  # Create
                # ドラッグアンドドロップでファイルパスを取得
                options = ["ファイルから入力", "キーボードで入力"]
                wayToInput = co.getInput(options)
                if wayToInput == 0:
                    filePath = fo.inputFile()
                    registeredData = fo.registerPickUpPoint(filePath)
                    if registeredData is not None:
                        
                        fo.printRegisteredData(registeredData)
                    else:
                        print("Error: データの登録に失敗しました。")
                elif wayToInput == 1:
                    new_name = co.getSingleStrInput("新しい名前を入力してください: ")
                    new_address = co.getSingleStrInput("新しい住所を入力してください: ")
                    pass

            elif crud_action == 1:  # Read
                fo.printAllPickupPoint()

            elif crud_action == 2:  # Update
                db = DatabaseManager('KidsDuoBusRouting.db')
                fo.printAllPickupPoint()
                id_list = co.getMultipleStrInput("更新したいデータのIDを入力してください: ")

                for id in id_list:
                    current_name = db.getPickupPoint(id)[1]
                    current_address = db.getPickupPoint(id)[2]

                    print(f"ID {id} の現在の名前は {current_name} で、現在の住所は {current_address} です。")

                    new_name = co.getSingleStrInput(f"ID {id} の新しい名前を入力してください: ")
                    new_address = co.getSingleStrInput(f"ID {id} の新しい住所を入力してください: ")
                    fo.updatePickupPoint(id, new_name, new_address)



            elif crud_action == 3:  # Delete
                fo.printAllPickupPoint()
                id_list = co.getMultipleStrInput("削除したいデータのIDを入力してください: ")
                for id in id_list:
                    fo.deletePickupPoint(id)

            elif crud_action == 4:  # Exit
                print("終了します。")
                break
        elif action == 2:  # Exit
            print("終了します。")
            break
