from ConsoleOperation import ConsoleOperation
from FileOperation import FileOperation
from BusRouting import BusRouting

NUMBER_OF_BUSES = 3
if __name__ == "__main__":
    co = ConsoleOperation()
    action = co.inputAction()

    if 1 <= action <= 2:
        # ファイル管理のためクラスインスタンスを作成
        fo = FileOperation()

        # ドラッグアンドドロップでファイルパスを取得
        filePath = fo.inputFile()

        # バスの経路を計算
        if action == 1:
            students = fo.setStudentData(filePath)

            br = BusRouting()

            br.executeBusRouting(students, NUMBER_OF_BUSES)

        # ピックアップポイントの定義
        elif action == 2:
            registeredData = fo.registerPickUpPoint(filePath)

            fo.printRegisteredData(registeredData)
    else:
        pass
