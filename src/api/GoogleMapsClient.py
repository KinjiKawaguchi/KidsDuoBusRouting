import requests
import json
from urllib.parse import quote

class GoogleMapsClient:
    def __init__(self):
        self.API_KEY = ""

    def calculate_duration(self, from_address, to_address):
        # URLエンコードを適用
        origin = quote(from_address)
        destination = quote(to_address)

        # APIリクエストのURLを作成
        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&key={self.API_KEY}"

        # APIリクエストを実行
        response = requests.get(url)

        # 応答をJSON形式でパース
        data = json.loads(response.text)

        # 応答から所要時間と距離を取得
        try:
            rows = data["rows"]
            elements = rows[0]["elements"]
            duration = elements[0]["duration"]["text"]
            distance = elements[0]["distance"]["text"]
        except KeyError:
            duration = None
            distance = None
        print(duration, distance)

        return duration, distance
