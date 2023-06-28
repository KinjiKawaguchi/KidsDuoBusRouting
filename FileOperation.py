import tkinter as tk  
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import csv
import Student

class FileOperation: 
    def __init__(self):  
        self.filepath = ''  
        self.root = TkinterDnD.Tk()

    def drop(self,event): 
        self.filepath = event.data 
        self.root.quit()

    def setupGUI(self):  # GUIの構成を行う新たなメソッドを作成
        self.frame = tk.Frame(self.root, name='drag-drop-area', width=400, height=400)  # Initialize the frame in the constructor
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
    
    def readCSV(self,file_path):
        if not os.path.exists(file_path):
            print("Error: ファイルが存在しません")
            return None

        if not os.path.isfile(file_path):
            print("Error: ファイルパスが無効です")
            return None

        if not file_path.endswith(".csv"):
            print("Error: CSVファイルではありません")
            return None

        students = []
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) < 3:
                        print("Error: データが不完全です")
                        return None

                    name = row[0]
                    address = row[1]
                    dismissal_time = row[2]

                    student = Student(name, address, dismissal_time)
                    students.append(student)

        except Exception as e:
            print(f"Error: ファイルの読み込み中にエラーが発生しました: {e}")
            return None

        return students