import csv
import os
import tkinter as tk

from tkinterdnd2 import DND_FILES, TkinterDnD

from BusRouting import BusRouting
from DatabaseManager import DatabaseManager
from GoogleMapsClient import GoogleMapsClient
from Student import Student


class FileOperation:
    APIKEY = ""

    def __init__(self):
        self.filepath = ''
        self.root = TkinterDnD.Tk()

    def drop(self, event):
        self.filepath = event.data
        self.root.quit()

    def setupGUI(self):  # GUIの構成を行う新たなメソッドを作成
        self.frame = tk.Frame(self.root, name='drag-drop-area', width=400,
                              height=400)  # Initialize the frame in the constructor
        self.frame.pack()
        self.root.update()
        self.root.dnd_accept = lambda x: x
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.frame.drop_target_register(DND_FILES)
        self.frame.dnd_bind('<<Drop>>', self.drop)

    def inputFile(self):
        self.root.withdraw()
        self.setupGUI()  # GUIの構成部分をここで呼び出す
        self.root.deiconify()
        self.root.mainloop()

        return self.filepath

    def readCSV(self, filePath, encodingType):
        print(f"ファイルパス: {filePath}")
        if not os.path.exists(filePath):
            print("Error: ファイルが存在しません")
            return None

        if not os.path.isfile(filePath):
            print("Error: ファイルパスが無効です")
            return None

        if not filePath.endswith(".csv"):
            print("Error: CSVファイルではありません")
            return None

        try:
            with open(filePath, "r", encoding=encodingType) as file:
                reader = csv.reader(file)
                return list(reader)
        except Exception as e:
            print(f"Error: CSVファイルの読み込み中にエラーが発生しました: {e}")
            return None

    def setStudentData(self, filePath):
        rows = self.readCSV(filePath, "utf-8")

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

    def registerPickUpPoint(self, filePath):
        # Use your actual database name
        db = DatabaseManager('KidsDuoBusRouting.db')

        # データベースが空の場合はユーザーに原点となる地点を入力してもらう
        if db.checkTableEmptyIs():
            while True:
                name = input('原点となる地点の名前を入力してください: ')
                address = input('原点となる地点の住所を入力してください: ')

                # ユーザーに入力を確認してもらう
                print(f"\n入力内容: \n名前: {name} \n住所: {address}")
                while True:
                    confirm = input("この情報でよろしいですか？ (yes/no): ").lower()
                    if confirm == "yes" or confirm == "no":
                        break
                if confirm == "yes":
                    addedPlace = db.addPlace(name, address)
                    if addedPlace != None:
                        pass
                    break
                else:
                    print("再度入力してください。")

        rows = self.readCSV(filePath, "utf-8")

        for row in rows:
            if len(row) != 2:
                print("Error: データが不正です。")
                return None

        registeredData = []
        for row in rows:
            name, address = row
            if db.checkPlaceExistsIs(name):
                print(f"Error: '{name}' already exists in the database.")
            else:
                addedPlaces = db.addPlace(name, address)
                for addedPlace in addedPlaces:
                    db.addRouteSegment()
                if addedPlaces != None:
                    pass
                registeredData.append(row)

        return registeredData

    def printRegisteredData(self, rows):
        print("登録されたデータは以下の通りです。")
        print("====================================")
        for row in rows:
            print(row[0], row[1])

    def printAllPickupPoint(self):
        db = DatabaseManager('KidsDuoBusRouting.db')
        places = db.getAllplaces()
        for place in places:
            print(f"ID: {place[0]}, Name: {place[1]}, Address: {place[2]}")

    def updatePickupPoint(self, id, new_name, new_address):
        db = DatabaseManager('KidsDuoBusRouting.db')
        updatedData = db.updatePlace(id, new_name, new_address)
        if updatedData != None:
            pass

    def deletePickupPoint(self, id):
        db = DatabaseManager('KidsDuoBusRouting.db')
        deletedData = db.deletePlace(id)
        if deletedData != None:
            pass

    def addRouteSegment(self, addedPlace):
        google = GoogleMapsClient()
        db = DatabaseManager('KidsDuoBusRouting.db')

        addedId = addedPlace[0]
        addedAddress = addedPlace[2]

        db.getRouteSegment(0)
        comparisonPlace = self.cursor.fetchone()

        while comparisonPlace != addedPlace:
            comparisonId = comparisonPlace[0]
            comparisonAddress = comparisonPlace[2]

            time, distance = google.getTravelTime(
                addedAddress, comparisonAddress)
            db.addRouteSegment(addedId, comparisonId, time, distance)

            time, distance = google.getTravelTime(
                comparisonAddress, addedAddress)
            db.addRouteSegment(comparisonId, addedId, time, distance)

            i = 1
            while not (self.checkPlaceExistsIs(comparisonPlace[0] + 1)):
                i += 1
            db.getRouteSegment(comparisonPlace[0] + i)
            comparisonPlace = self.cursor.fetchone()
        self.conn.commit()
