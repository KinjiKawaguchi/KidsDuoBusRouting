import os
import json
from cryptography.fernet import Fernet


class APIKeyManager:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.key = self.get_or_create_key()

    def get_or_create_key(self):
        # キーが設定ファイルに存在する場合、それを読み取る
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as file:
                config_data = json.load(file)
                key = config_data.get("crypto_key")
        else:
            # キーが存在しない場合は新たに生成して設定ファイルに保存
            key = Fernet.generate_key().decode()
            config_data = {"crypto_key": key}
            with open(self.config_path, "w") as file:
                json.dump(config_data, file)
            print("初回起動設定が終了しました。再起動してください。")
            exit(0)  # ここでプログラムを終了

        return key.encode()

    def encrypt_api_key(self, api_key):
        cipher = Fernet(self.key)
        encrypted_api_key = cipher.encrypt(api_key.encode())
        return encrypted_api_key

    def decrypt_api_key(self, encrypted_api_key):
        cipher = Fernet(self.key)
        decrypted_api_key = cipher.decrypt(encrypted_api_key).decode()
        return decrypted_api_key
