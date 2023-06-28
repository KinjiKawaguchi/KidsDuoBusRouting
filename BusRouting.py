import requests
import Bus
import Student

class BusRouting:
    def __init__(self):
        self.students = []
        self.bus = []
        
    def executeBusRouting(self, students):
        self.students = students
        
    def get_travel_time(origin, destination, api_key):
        base_url = "https://maps.googleapis.com/maps/api/directions/json?"

        # パラメータをURLに組み組み込む
        complete_url = f"{base_url}origin={origin}&destination={destination}&key={api_key}"
        
        # APIを呼び出す
        response = requests.get(complete_url)

        #応答の確認
        response.raise_for_status()

        # 応答からJSONを取得
        directions = response.json()

        # ルートのリストから最初の提案を取得
        route = directions['routes'][0]

        # ルートからレッグのリストを取得し、最初のレッグ（通常は唯一のレッグ）を取得
        leg = route['legs'][0]

        # レッグから所要時間を取得
        duration = leg['duration']

        # 所要時間をリターン
        return duration['text']