import requests
import matplotlib.pyplot as plt
import numpy as np


api_key = "0iKaDKQrdMpKRS2LVhDifNC8QxMWDASPp9HVlnB7"
headers = {"X-API-KEY": api_key}

data_list = []
limited_years = [2012, 2016]


def get_data():
    for year in limited_years:
        response = requests.get(
            f"https://opendata.resas-portal.go.jp/api/v1/municipality/value/perYear?simcCode=51&cityCode=04100&year={year}&prefCode=4&sicCode=I",
            headers=headers,
        )
        data = response.json()
        data_list.append(data["result"]["data"][0]["value"])
    return data_list


# https://qiita.com/Sei123/items/b825abae8ba6cf3eb0ff
def main():
    get_data()
    print(data_list)
    fig, ax = plt.subplots()
    ax.plot(limited_years, data_list)
    plt.show()


if __name__ == "__main__":
    main()


# やること→1️⃣産業大分類を行列化→大分類を入力すると選択可
# 2️⃣市町村名をいれるとコードを取得して選択できる
# 最小二乗法で将来予想→グラフ もしくはグラフだけでいいかも(年数が少ないので)
