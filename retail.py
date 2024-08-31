import requests
from flask import Flask, render_template, request
import matplotlib
import numpy as np
from pref_cities import get_city_code2
from lsm2 import forecast_and_plot_svr
import io
import base64
import matplotlib.pyplot as plt

api_key = "0iKaDKQrdMpKRS2LVhDifNC8QxMWDASPp9HVlnB7"
headers = {"X-API-KEY": api_key}
app = Flask(__name__)
matplotlib.use("Agg")


def retail_sells(prefCode, cityCode):
    base_url = "https://opendata.resas-portal.go.jp/api/v1/municipality/sales/perYear?"
    params = f"cityCode={cityCode}&dispType=1&simcCode=-&prefCode={prefCode}&sicCode=-"
    url = base_url + params
    response = requests.get(url, headers=headers)
    data = response.json()
    data_list = []
    years = []
    for item in data["result"]["data"]:
        data_list.append(item["value"])
        years.append(item["year"])
    return data_list, years


@app.route("/2", methods=["GET", "POST"])
def show_graph2():
    if request.method == "GET":
        return render_template("index3.html")
    else:
        prefName = request.form["prefName"]
        cityName = request.form["cityName"]
        prefCode, cityCode = get_city_code2(prefName, cityName)
        data_list, years = retail_sells(prefCode, cityCode)
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
        img = io.BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode("utf-8")
        return render_template("index.html", image_data=img_base64, prefName=prefName, cityName=cityName)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
