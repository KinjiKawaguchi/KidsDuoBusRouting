from calc_travel_time import get_travel_time
from get_file import GetFile

if __name__ == "__main__":
    getFile = GetFile()
    dropped_file_path = getFile.run()
    print(f"ドロップされたファイル: {dropped_file_path}")
    
    api_key = "YOUR_API_KEY"#環境変数が良い
    origin = "KidsDuo佐鳴台"
    destination = "静岡大学情報学部,母"

    duration = get_travel_time(origin, destination, api_key)
    print(f"The estimated travel time is {duration}.")