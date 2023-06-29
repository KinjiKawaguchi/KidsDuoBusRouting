class ConsoleOperation:
    def inputAction(self):
        options = ["バス経路の出力", "ピックアップポイントの設定"]
        while True:
            for i in range(len(options)):
                print(str(i) + "." + options[i])
            action = int(input(">>"))
            if 0 <= action <= len(options) - 1:
                break
        return action