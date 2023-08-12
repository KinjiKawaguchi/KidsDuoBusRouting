import sys
import bcrypt

from src.db.PlaceDatabaseManager import PlaceDatabaseManager


class ConsoleOperation:
    """-------------入力を受け取りメソッド類-------------"""
    def receive_input(self, options):
        while True:
            try:
                index = int(input(">> "))
                if 1 <= index <= len(options):
                    if self._confirm_action(options[index - 1]):
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
                if self._confirm_action(user_input):
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
                if self._confirm_action(user_input):
                    return [string.strip() for string in user_input.split()]
                else:
                    print("再度入力してください。")
            print("入力してください。")

    @staticmethod
    def _confirm_action(action):
        while True:
            is_confirm = input(
                f"選択されたのは、{action}です。 この操作でよろしいですか？ (yes/no): ").lower()
            if is_confirm in ["yes", "no"]:
                return is_confirm == "yes"

    @staticmethod
    def receive_yes_or_no_input(message):
        while True:
            is_confirm = input(f"{message} (yes/no): ").lower()
            if is_confirm in ["yes", "no"]:
                return is_confirm == "yes"

    """-------------メニュー表示類-------------"""
    def login_or_register(self, fo):
        if not fo.has_user_records():
            self._register_or_exit(fo)

        username = fo.get_current_username()
        if username:
            username = self._handle_logged_in_user(fo, username)
            if not username:
                self.login_or_register(fo)
        else:
            return self._handle_login_or_register_menu(fo)
    
    def handle_main_menu(self, fo):
        while True:
            main_menu_options = ["バスの経路を計算",
                                 "ピックアップポイントのデータ管理", "ルートセグメントのデータ管理", "終了"]
            self.print_menu("KidsDuoバスルーティングシステム", main_menu_options)
            action = self.receive_input(main_menu_options)

            if action == 1:
                self.handle_bus_route_calculation()
            elif action == 2:
                self.handle_pickup_point_management(fo)
            elif action == 3:
                self.handle_route_segment_management(fo)
            elif action == 4:
                self.exit()
            else:
                self.print_unexpected_input_message()
            input("Enterを押してください。")

    def handle_bus_route_calculation(self):
        self.print_unimplemented_message()
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
            self.handle_route_segment_update()
        elif crud_action == 3:
            self.exit()

    """-------------ユーザー操作類-------------"""
    def _register_or_exit(self, fo):
        options = ["新規ユーザー登録", "終了"]
        self.print_menu("新規登録", options)
        action = self.receive_input(options)
        if action == 1:
            self._register_user(fo)
        else:
            self.exit()

    def _handle_logged_in_user(self, fo, username):
        options = ["ログアウトする", "続ける", "終了する"]
        self.print_menu(f"ログイン中: {username}", options)
        choice = self.receive_input(options)
        if choice == 1:
            fo.logout()
            return None
        elif choice == 2:
            return username
        elif choice == 3:
            self.exit()

    def _handle_login_or_register_menu(self, fo):
        while True:
            options = ["ログイン", "ユーザ登録", "終了"]
            self.print_menu("ログイン", options)
            action = self.receive_input(options)
            if action == 1:
                return self._login(fo)
            elif action == 2:
                self._register_user(fo)
            else:
                self.exit()

    def _register_user(self, fo):
        while True:
            username = self.receive_single_str_input("ユーザ名を入力してください: ")
            password = self.receive_single_str_input("パスワードを入力してください: ")
            hashed_password = self._hash_password(password)
            api_key = self.receive_single_str_input("Google Maps APIキーを入力してください: ")
            encrypted_key = fo.akm.encrypt_api_key(api_key)
            keep_logged_in = self.receive_yes_or_no_input("ログイン状態を維持しますか？(y/n): ")

            if fo.add_user(username, hashed_password, encrypted_key, keep_logged_in):
                print("ユーザの登録に成功しました。")
                break

            self._handle_registration_failure(fo)

    def _handle_registration_failure(self, fo):
        print("ユーザの登録に失敗しました。")
        input("Enterを押してください。")
        options = ["再入力", "終了"]
        self.print_menu("ユーザ登録", options)
        action = self.receive_input(options)
        if action == 2:
            self.exit()

    def _login(self, fo):
        while True:
            username = self.receive_single_str_input("ユーザ名を入力してください: ")
            password = self.receive_single_str_input("パスワードを入力してください: ")

            if fo.authenticate(username, password):
                print("ログインに成功しました。")
                return username

            self._handle_login_failure(fo)

    def _handle_login_failure(self, fo):
        print("ログインに失敗しました。ユーザ名またはパスワードが間違っています。")
        input("Enterを押してください。")
        options = ["再入力", "新規ユーザー登録", "終了"]
        self.print_menu("ログイン", options)
        action = self.receive_input(options)
        if action == 2:
            self._register_user(fo)
        elif action == 3:
            self.exit()

    @staticmethod
    def _hash_password(password: str) -> bytes:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt)

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
            self.print_unimplemented_message()
            pass
        elif input_way == 3:
            self.exit()

    def handle_pickup_point_update(self, fo):
        pickup_points = fo.print_all_pickup_point()
        db = PlaceDatabaseManager('KidsDuoBusRouting.db')
        if pickup_points is not None:
            pickup_point_id_list = self.receive_multiple_str_input(
                "更新したいデータのIDを入力してください: ")
            for pickup_point_id in pickup_point_id_list:
                current_data = fo.get_pickup_point(pickup_point_id)
                if current_data is None:
                    self.print_no_data_message()
                else:
                    print(
                        f"ID {pickup_point_id} \n,"
                        f"名前: {current_data[db.PP_NAME_COLUMN]}\n,"
                        f"住所: {current_data[db.PP_ADDRESS_COLUMN]} \n,"
                        f"原点ピックアップポイント:{current_data[db.PP_IS_ORIGIN_COLUMN]}\n,"
                        f"待てる場所か:{current_data[db.PP_CAN_WAIT_COLUMN]}")

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

    def handle_route_segment_update(self):
        self.print_unimplemented_message()
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

    @staticmethod
    def print_menu(title, options):
        print("=" * 36)
        print(title)
        print("=" * 36)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

    @staticmethod
    def exit():
        print("終了します。")
        sys.exit(0)

    def print_unexpected_input_message(self):
        self.print_error_message("入力された値が不正です。")

    def print_no_data_message(self):
        self.print_error_message("データが存在しません。")

    def fail_to_register_message(self):
        self.print_error_message("データの登録に失敗しました。")
        
    def print_unimplemented_message(self):
        self.print_error_message("この機能は未実装です。")

    @staticmethod
    def print_error_message(message):
        print(f"Error: {message}")
