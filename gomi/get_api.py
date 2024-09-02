import requests

api_key = "0iKaDKQrdMpKRS2LVhDifNC8QxMWDASPp9HVlnB7"
headers = {"X-API-KEY": api_key}


response = requests.get("https://opendata.resas-portal.go.jp/api/v1/prefectures", headers=headers)
data = response.json()


# https://qiita.com/Sei123/items/b825abae8ba6cf3eb0ff
def main():

    print(data)


if __name__ == "__main__":
    main()
