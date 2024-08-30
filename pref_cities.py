import requests

api_key = "0iKaDKQrdMpKRS2LVhDifNC8QxMWDASPp9HVlnB7"
headers = {"X-API-KEY": api_key}


def get_city_code():
    prefName = input("都道府県名を入れてください:")
    response = requests.get("https://opendata.resas-portal.go.jp/api/v1/prefectures", headers=headers)
    data_dict = response.json()
    pref_dict = {item["prefName"]: item["prefCode"] for item in data_dict["result"]}
    cityName = input("市町村を入れてください。:")
    prefCode = pref_dict[prefName]
    response = requests.get(
        f"https://opendata.resas-portal.go.jp/api/v1/cities?prefCode={prefCode}", headers=headers
    )
    data_dict2 = response.json()
    city_code_dict = {item["cityName"]: item["cityCode"] for item in data_dict2["result"]}
    return prefCode, city_code_dict.get(cityName)


def get_city_code2(prefName, cityName):
    response = requests.get("https://opendata.resas-portal.go.jp/api/v1/prefectures", headers=headers)
    data_dict = response.json()
    pref_dict = {item["prefName"]: item["prefCode"] for item in data_dict["result"]}
    prefCode = pref_dict[prefName]
    response = requests.get(
        f"https://opendata.resas-portal.go.jp/api/v1/cities?prefCode={prefCode}", headers=headers
    )
    data_dict2 = response.json()
    city_code_dict = {item["cityName"]: item["cityCode"] for item in data_dict2["result"]}
    return prefCode, city_code_dict.get(cityName)


# https://qiita.com/Sei123/items/b825abae8ba6cf3eb0ff
def main():

    print(get_city_code())


if __name__ == "__main__":
    main()
