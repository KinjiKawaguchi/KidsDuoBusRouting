import csv
import os
import tkinter as tk

from tkinterdnd2 import DND_FILES, TkinterDnD

from DatabaseManager import DatabaseManager
from Student import Student


class FileOperation:
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

    def readCSV(self, file_path,encodingType):
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
            with open(file_path, "r", encoding=encodingType) as file:
                rows = csv.reader(file)
        except Exception as e:
            print(f"Error: ファイルの読み込み中にエラーが発生しました: {e}")
            return None
        return rows

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
        db = DatabaseManager('KidsDuoBusRouting.db')  # Use your actual database name
        rows = self.readCSV(filePath, "utf-8")

        for row in rows:
            if len(row) != 2:
                print("Error: データが不正です。")
                return None

        for row in rows:
            name, address = row
            if db.check_place_exists(name, address):
                print(f"Error: '{name}' or '{address}' already exists in the database.")
            else:
                db.add_place(name, address)

        return rows

    def printRegisteredData(self, rows):
        print("登録されたデータは以下の通りです。")
        print("====================================")
        for row in rows:
            print(row[0], row[1])
