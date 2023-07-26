class ConsoleOperation:
    def receive_input(self,options):
        while True:
            for i in range(len(options)):
                print(str(i) + "." + options[i])
            index = int(input(">>"))
            if 0 <= index <= len(options) - 1:
                while True:
                    print("選択されたのは" + options[index] + "です。")
                    is_confirm = input("この操作でよろしいですか？ (yes/no): ").lower()
                    if is_confirm == "yes" or is_confirm == "no":
                        if is_confirm == "yes":
                            return index
                        else:
                            print("再度入力してください。")
                            break

    def receive_single_str_input(self, message):
        while True:
            input = input(message)
            if input == "":
                print("入力してください。")
            else:
                while True:
                    print("入力されたのは" + input + "です。")
                    confirm = input("この操作でよろしいですか？ (yes/no): ").lower()
                    if confirm == "yes" or confirm == "no":
                        if confirm == "yes":
                            return input
                        else:
                            print("再度入力してください。")
                            break

    def receive_multiple_str_input(self, message):
        while True:
            input = input(message + " (複数のIDを入力する場合はスペースで区切ってください): ")
            if input == "":
                print("入力してください。")
            else:
                input_list = [str.strip() for str in input.split()]
                while True:
                    print("入力されたのは" + ", ".join(input_list) + "です。")
                    is_confirm = input("この操作でよろしいですか？ (yes/no): ").lower()
                    if is_confirm == "yes" or is_confirm == "no":
                        if is_confirm == "yes":
                            return input_list
                        else:
                            print("再度入力してください。")
                            break
