import requests
import matplotlib.pyplot as plt


api_key = "0iKaDKQrdMpKRS2LVhDifNC8QxMWDASPp9HVlnB7"
headers = {"X-API-KEY": api_key}


limited_years = [2012, 2016]


def get_data(prefCode, cityCode, y):
    data_list = []
    for year in limited_years:
        base_url = "https://opendata.resas-portal.go.jp/api/v1/municipality/value/perYear?simcCode="
        params = f"-&cityCode={cityCode}&year={year}&prefCode={prefCode}&sicCode=-"
        url = base_url + params
        response = requests.get(url, headers=headers)
        data = response.json()
        print(data)
        try:
            data_list.append(data["result"]["data"][0]["value"])
        except (KeyError, IndexError):
            data_list.append(0)  # Append 0 if error occurs
    return data_list


# https://qiita.com/Sei123/items/b825abae8ba6cf3eb0ff
def main():
    limited_years = [2012, 2016]
    prefCode = "3"
    cityCode = "03201"
    data_list = get_data(prefCode, cityCode, limited_years)
    print(data_list)
    fig, ax = plt.subplots()
    ax.plot(limited_years, data_list)
    plt.show()


if __name__ == "__main__":
    main()


# やること→1️⃣産業大分類を行列化→大分類を入力すると選択可
# 2️⃣市町村名をいれるとコードを取得して選択できる
# 最小二乗法で将来予想→グラフ もしくはグラフだけでいいかも(年数が少ないので)
