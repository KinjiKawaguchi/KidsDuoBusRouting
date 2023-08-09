import sys

from db.DatabaseManager import DatabaseManager


class ConsoleOperation:
    """-------------入力を受け取りメソッド類-------------"""

    def receive_input(self, options):
        while True:
            try:
                index = int(input(">> "))
                if 1 <= index <= len(options):
                    if self.confirm_action(options[index - 1]):
                        return index
                    else:
                        self.print_error_message("再度入力してください。")
                else:
                    self.print_error_message("入力された値が不正です。")
            except ValueError:
                self.print_error_message("数値を入力してください。")

    def receive_single_str_input(self, message):
        while True:
            user_input = input(message).strip()
            if user_input:
                if self.confirm_action(user_input):
                    return user_input
                else:
                    print("再度入力してください。")
            else:
                print("入力してください。")

    def receive_multiple_str_input(self, message):
        while True:
            user_input = input(
                f"{message} (複数のIDを入力する場合はスペースで区切ってください): ").strip()
            if user_input:
                if self.confirm_action(user_input):
                    return [str.strip() for str in user_input.split()]
                else:
                    print("再度入力してください。")
            print("入力してください。")

    def confirm_action(self, action):
        while True:
            is_confirm = input(
                f"選択されたのは、{action}です。 この操作でよろしいですか？ (yes/no): ").lower()
            if is_confirm in ["yes", "no"]:
                return is_confirm == "yes"

    """-------------メニュー表示類-------------"""

    def handle_main_manu(self, fo):
        while True:
            main_menu_options = ["バスの経路を計算",
                                 "ピックアップポイントのデータ管理", "ルートセグメントのデータ管理", "終了"]
            self.print_menu("KidsDuoバスルーティングシステム", main_menu_options)
            action = self.receive_input(main_menu_options)

            if action == 1:
                self.handle_bus_route_calculation(fo)
            elif action == 2:
                self.handle_pickup_point_management(fo)
            elif action == 3:
                self.handle_route_segment_management(fo)
            elif action == 4:
                self.exit()
            else:
                self.print_unexpected_input_message()

    def handle_bus_route_calculation(self, fo):
        print("バスのルート設計機能は未実装です。")
        pass
        """
        file_path = fo.receive_file()
        students = fo.instantiate_student(file_path)
        br = BusRouting()
        br.determining_bus_route(students, NUMBER_OF_BUSES)
        """

    def handle_pickup_point_management(self, fo):
        options = ["登録", "表示", "更新", "削除", "終了"]
        self.print_menu("ピックアップポイントのデータ管理", options)
        crud_action = self.receive_input(options)
        if crud_action == 1:  # Create
            self.handle_pickup_point_creation(fo)
        elif crud_action == 2:  # Read
            fo.print_all_pickup_point()
        elif crud_action == 3:  # Update
            self.handle_pickup_point_update(fo)
        elif crud_action == 4:  # Delete
            self.handle_pickup_point_deletion(fo)
        elif crud_action == 5:  # Exit
            self.exit()
        else:
            self.print_unexpected_input_message()

    def handle_route_segment_management(self, fo):
        options = ["表示", "更新", "終了"]
        self.print_menu("ルートセグメントのデータ管理", options)
        crud_action = self.receive_input(options)
        if crud_action == 1:
            fo.print_all_route_segment()
        elif crud_action == 2:
            self.handle_route_segment_update(fo)
        elif crud_action == 3:
            self.exit()

    """-------------ピックアップポイント操作類-------------"""

    def handle_pickup_point_creation(self, fo):
        options = ["ファイルから入力", "キーボードで入力", "終了"]
        self.print_menu("ピックアップポイントの登録", options)
        input_way = self.receive_input(options)
        if input_way == 1:
            file_path = fo.receive_file()
            registered_data = fo.register_pickup_point(file_path)
            if registered_data is not None:
                fo.print_registered_data(registered_data)
            else:
                self.fail_to_register_message()
        elif input_way == 2:
            print("キーボードからの入力は現在未実装です。")
            pass
        elif input_way == 3:
            self.exit()

    def handle_pickup_point_update(self, fo):
        pickup_points = fo.print_all_pickup_point()
        db = DatabaseManager('KidsDuoBusRouting.db')
        if pickup_points is not None:
            pickup_point_id_list = self.receive_multiple_str_input(
                "更新したいデータのIDを入力してください: ")
            for pickup_point_id in pickup_point_id_list:
                current_data = fo.get_pickup_point(pickup_point_id)
                if current_data is None:
                    self.print_no_data_message()
                else:
                    print(
                        f"ID {pickup_point_id} \n名前: {current_data[db.PP_NAME_COLUMN]}\n住所: {current_data[db.PP_ADDRESS_COLUMN]} \n原点ピックアップポイント:{current_data[db.PP_IS_ORIGIN_COLUMN]}\n待てる場所か:{current_data[db.PP_CAN_WAIT_COLUMN]}")

                    new_name = self.receive_single_str_input(
                        f"ID {pickup_point_id} の新しい名前を入力してください: ")
                    new_address = self.receive_single_str_input(
                        f"ID {pickup_point_id} の新しい住所を入力してください:")
                    new_can_wait = self.receive_single_str_input(
                        f"ID {pickup_point_id} の待てる場所かを入力してください: ")

                    fo.update_pickup_point(
                        pickup_point_id, new_name, new_address, new_can_wait)
                    print(f"ID {pickup_point_id} のデータを更新しました。")

    def handle_pickup_point_deletion(self, fo):
        pickup_points = fo.print_all_pickup_point()
        if pickup_points is not None:
            pickup_point_id_list = self.receive_multiple_str_input(
                "削除したいデータのIDを入力してください:  ")
            for pickup_point_id in pickup_point_id_list:
                fo.delete_pickup_point(pickup_point_id)

    """-------------ルートセグメント操作類-------------"""

    def handle_route_segment_update(self, fo):
        print("ルートセグメント情報を直接編集する機能は未実装です。")
        pass
        """
        route_segments = fo.print_all_route_segment()
        if route_segments is not None:
            pickup_point_id_list = self.receive_multiple_str_input("更新するデータのIDを入力してください。(複数可):")
            for pickup_point_id in pickup_point_id_list:
                segment_data = fo.get_route_segment(pickup_point_id=pickup_point_id)
                origin_name = fo.get_pickup_point(segment_data[5])[1]
                destination_name = fo.get_pickup_point(segment_data[6])[1]
                current_duration = segment_data[3]
                current_distance = segment_data[4]

                print(f"ID {pickup_point_id} の出発地点は {origin_name}で、到着地点は{destination_name} です。")
                print(f"現在登録されている所要時間は {current_duration}分で、現在登録されている距離は{current_distance} km です。")

                new_duration = self.receive_single_str_input(f"ID {pickup_point_id}に対して新しく登録する所要時間を入力: ")
                new_distance = self.receive_single_str_input(f"ID {pickup_point_id}に対して新しく登録する距離を入力: ")

                fo.update_route_segment(pickup_point_id, new_duration, new_distance)
                print(f"ID {pickup_point_id} のデータを更新しました。")
        """

    """-------------単純出力・操作類-------------"""

    def print_menu(self, title, options):
        print("=" * 36)
        print(title)
        print("=" * 36)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

    def exit(self):
        print("終了します。")
        sys.exit(0)

    def print_unexpected_input_message(self):
        self.print_error_message("入力された値が不正です。")

    def print_no_data_message(self):
        self.print_error_message("データが存在しません。")

    def fail_to_register_message(self):
        self.print_error_message("データの登録に失敗しました。")

    def print_error_message(self, message):
        print(f"Error: {message}")
