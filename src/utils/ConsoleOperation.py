class ConsoleOperation:
    def receive_input(self,options):
        global index
        index = 0
        while True:
            for i in range(len(options)):
                print(str(i + 1) + "." + options[i])
            try:
                index = int(input(">> "))
            except ValueError:
                print("数字を入力してください。")
            if 1 <= index <= len(options):
                while True:
                    print("選択されたのは" + options[index - 1] + "です。")
                    is_confirm = input("この操作でよろしいですか？ (yes/no): ").lower()
                    if is_confirm == "yes" or is_confirm == "no":
                        if is_confirm == "yes":
                            return index
                        else:
                            print("再度入力してください。")
                            break
            else:
                print("選択肢の中にある数字を選んでください。")
                
    def receive_single_str_input(self, message):
        while True:
            user_input = input(message)
            if user_input == "":
                print("入力してください。")
            else:
                while True:
                    print("入力されたのは" + user_input + "です。")
                    confirm = input("この操作でよろしいですか？ (yes/no): ").lower()
                    if confirm == "yes" or confirm == "no":
                        if confirm == "yes":
                            return user_input
                        else:
                            print("再度入力してください。")
                            break

    def receive_multiple_str_input(self, message):
        while True:
            user_input = input(f"{message} (複数のIDを入力する場合はスペースで区切ってください): ")

            if user_input == "":
                print("入力してください。")
            else:
                input_list = [str.strip() for str in user_input.split()]
                while True:
                    print("入力されたのは" + ", ".join(input_list) + "です。")
                    is_confirm = input("この操作でよろしいですか？ (yes/no): ").lower()
                    if is_confirm == "yes" or is_confirm == "no":
                        if is_confirm == "yes":
                            return input_list
                        else:
                            print("再度入力してください。")
                            break
