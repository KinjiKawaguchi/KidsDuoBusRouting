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
