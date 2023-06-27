import tkinter as tk  
from tkinterdnd2 import DND_FILES, TkinterDnD  

class GetFile: 
    def __init__(self):  
        self.filepath = ''  
        self.root = TkinterDnD.Tk()  
        self.frame = tk.Frame(self.root, name='drag-drop-area', width=400, height=400)  # Initialize the frame in the constructor

    def drop(self,event): 
        self.filepath = event.data 
        self.root.quit()

    def setup_gui(self):  # GUIの構成を行う新たなメソッドを作成
        self.frame.pack()  
        self.root.update() 
        self.root.dnd_accept = lambda x: x
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy) 
        self.frame.drop_target_register(DND_FILES)  
        self.frame.dnd_bind('<<Drop>>', self.drop)

    def run(self):  
        self.root.withdraw() 
        self.setup_gui()  # GUIの構成部分をここで呼び出す
        self.root.deiconify()  
        self.root.mainloop()  

        return self.filepath
