import requests
from flask import Flask, render_template, request
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from pref_cities import get_city_code2
from lsm2 import forecast_and_plot_svr
import io
import base64

api_key = "0iKaDKQrdMpKRS2LVhDifNC8QxMWDASPp9HVlnB7"
headers = {"X-API-KEY": api_key}
app = Flask(__name__)
matplotlib.use("Agg")


def population(prefCode, cityCode):
    base_url = "https://opendata.resas-portal.go.jp/api/v1/population/composition/perYear?"
    params = f"cityCode={cityCode}&prefCode={prefCode}"
    url = base_url + params
    response = requests.get(url, headers=headers)
    data = response.json()
    data_list = []
    years = []
    for item in data["result"]["data"]:
        if item["label"] == "総人口":
            for data_point in item.get("data", [0]):
                if "value" in data_point and "year" in data_point:
                    data_list.append(data_point["value"])
                    years.append(data_point["year"])
    return data_list, years


@app.route("/")
def home():
    return "Welcome to the Population Forecast App!"


@app.route("/2", methods=["GET", "POST"])
def show_graph2():
    if request.method == "GET":
        return render_template("index3.html")
    else:
        plt.clf()
        plt.close('all')
        prefName = request.form["prefName"]
        cityName = request.form["cityName"]
        prefCode, cityCode = get_city_code2(prefName, cityName)
        data_list, years = population(prefCode, cityCode)
        y = np.array(data_list)  # NumPy配列に変換
        x = np.array(years)
        X_forecast, y_forecast = forecast_and_plot_svr(x, y)

        # プロットを作成
        plt.figure(figsize=(12, 6))
        plt.scatter(x, y, color="darkorange", label="Actual data")
        plt.plot(X_forecast, y_forecast, color="navy", label="SVR prediction")
        plt.xlabel("Year")
        plt.ylabel("Population")
        plt.title(f"Population Forecast for {cityName}, {prefName}")
        plt.legend()
        plt.grid(True)

        # 画像を保存し

        # 画像を保存し、Base64エンコード
        img = io.BytesIO()
        plt.savefig(img, format="png")
        plt.close()  # メモリリークを防ぐためにfigureを閉じる
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode("utf-8")

        return render_template("index.html", image_data=img_base64, prefName=prefName, cityName=cityName)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
