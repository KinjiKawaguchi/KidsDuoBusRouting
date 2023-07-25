class ConsoleOperation:
    def getInput(self,options):
        while True:
            for i in range(len(options)):
                print(str(i) + "." + options[i])
            index = int(input(">>"))
            if 0 <= index <= len(options) - 1:
                while True:
                    print("選択されたのは" + options[index] + "です。")
                    confirm = input("この操作でよろしいですか？ (yes/no): ").lower()
                    if confirm == "yes" or confirm == "no":
                        if confirm == "yes":
                            return index
                        else:
                            print("再度入力してください。")
                            break

    def getSingleStrInput(self, message):
        while True:
            strInput = input(message)
            if strInput == "":
                print("入力してください。")
            else:
                while True:
                    print("入力されたのは" + strInput + "です。")
                    confirm = input("この操作でよろしいですか？ (yes/no): ").lower()
                    if confirm == "yes" or confirm == "no":
                        if confirm == "yes":
                            return strInput
                        else:
                            print("再度入力してください。")
                            break

    def getMultipleStrInput(self, message):
        while True:
            strInput = input(message + " (複数のIDを入力する場合はスペースで区切ってください): ")
            if strInput == "":
                print("入力してください。")
            else:
                strList = [str.strip() for str in strInput.split()]
                while True:
                    print("入力されたのは" + ", ".join(strList) + "です。")
                    confirm = input("この操作でよろしいですか？ (yes/no): ").lower()
                    if confirm == "yes" or confirm == "no":
                        if confirm == "yes":
                            return strList
                        else:
                            print("再度入力してください。")
                            break
