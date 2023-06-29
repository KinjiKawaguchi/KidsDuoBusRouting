from ConsoleOperation import ConsoleOperation
from FileOperation import FileOperation
from BusRouting import BusRouting

NUMBER_OF_BUSES = 3
if __name__ == "__main__":
    co = ConsoleOperation()
    options = ["バスの経路を計算", "ピックアップポイントのデータ管理"]
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
        options = ["登録", "表示", "更新", "削除"]
        crud_action = co.getInput(options)

        if crud_action == 0:  # Create
            # ドラッグアンドドロップでファイルパスを取得
            filePath = fo.inputFile()
            fo.registerPickUpPoint(filePath)

        elif crud_action == 1:  # Read
            fo.printPickupPoint()

        elif crud_action == 2:  # Update
            id = co.getSelectedDataIndex()
            new_name = co.inputNewName()
            new_address = co.inputNewAddress()
            fo.update_pickup_point(id, new_name, new_address)

        elif crud_action == 3:  # Delete
            id = co.getSelectedDataIndex()
            fo.delete_pickup_point(id)
    else:
        pass
