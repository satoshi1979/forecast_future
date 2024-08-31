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
years = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]


def asset_value(prefCode, cityCode, type):
    years = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
    data_list = []
    for year in years:
        base_url = "https://opendata.resas-portal.go.jp/api/v1/townPlanning/estateTransaction/bar?"
        params = f"year={year}&prefCode={prefCode}&cityCode={cityCode}&displayType={type}"
        url = base_url + params
        response = requests.get(url, headers=headers)
        data = response.json()
        try:
            data_list.append(data["result"]["years"][0]["value"])
        except (KeyError, IndexError):
            data_list.append(0)  # Append 0 if error occurs
    return data_list


# https://qiita.com/Sei123/items/b825abae8ba6cf3eb0ff, methods=["GET", "POST"]


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
        data_list = asset_value(prefCode, cityCode, "1")
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
        # 画像を保存し、Base64エンコード
        img = io.BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode("utf-8")
    return render_template("index.html", image_data=img_base64)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
