import matplotlib
import base64
from pref_cities import get_city_code2
from flask import Flask, render_template, request
import io
import numpy as np
import requests
from lsm2 import forecast_and_plot_svr
import matplotlib.pyplot as plt

# 共通
api_key = "0iKaDKQrdMpKRS2LVhDifNC8QxMWDASPp9HVlnB7"
headers = {"X-API-KEY": api_key}
limited_years = [2012, 2016]
app = Flask(__name__)
matplotlib.use("Agg")


# top
@app.route("/")
def top():
    return render_template("top.html")


# 付加価値額
def get_data_fukakachi(prefCode, cityCode, y):
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


@app.route("/fukakachi", methods=["GET", "POST"])
def show_hukakachi():
    if request.method == "GET":
        # img_base64 = make_graph()
        return render_template("index2.html")
    else:
        plt.clf()
        plt.close("all")
        prefName = request.form["prefName"]
        cityName = request.form["cityName"]
        prefCode, cityCode = get_city_code2(prefName, cityName)
        limited_years = [2012, 2016]
        data_list = get_data_fukakachi(prefCode, cityCode, limited_years)
        y = np.array(data_list)  # NumPy配列に変換
        x = np.array(limited_years)
        X_forecast, y_forecast = forecast_and_plot_svr(x, y)
        Title = "の付加価値額(企業単位)"
        # プロットを作成
        plt.figure(figsize=(12, 6))
        plt.scatter(x, y, color="darkorange", label="Actual data")
        plt.plot(X_forecast, y_forecast, color="navy", label="SVR prediction")
        plt.xlabel("Year")
        plt.ylabel("Added Value(Unit: 10,000 yen)")
        plt.legend()
        plt.grid(True)
        # 画像を保存し、Base64エンコード
        img = io.BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode("utf-8")
        return render_template(
            "index.html", image_data=img_base64, prefName=prefName, cityName=cityName, Title=Title
        )


# 付加価値額ここまで
# 製造業出荷額


def seizou_syukka(prefCode, cityCode):
    base_url = "https://opendata.resas-portal.go.jp/api/v1/municipality/manufacture/perYear?"
    params = f"cityCode={cityCode}&simcCode=-&prefCode={prefCode}&sicCode=-"
    url = base_url + params
    response = requests.get(url, headers=headers)
    data = response.json()
    data_list = []
    years = []
    for item in data["result"]["data"]:
        data_list.append(item["value"])
        years.append(item["year"])
    return data_list, years


@app.route("/syukka", methods=["GET", "POST"])
def show_syukka():
    if request.method == "GET":
        # img_base64 = make_graph()
        return render_template("index2.html")
    else:
        plt.clf()
        plt.close("all")
        prefName = request.form["prefName"]
        cityName = request.form["cityName"]
        prefCode, cityCode = get_city_code2(prefName, cityName)
        data_list, years = seizou_syukka(prefCode, cityCode)
        y = np.array(data_list)  # NumPy配列に変換
        x = np.array(years)
        X_forecast, y_forecast = forecast_and_plot_svr(x, y)

        # プロットを作成
        plt.figure(figsize=(12, 6))
        plt.scatter(x, y, color="darkorange", label="Actual data")
        plt.plot(X_forecast, y_forecast, color="navy", label="SVR prediction")
        Title = "製造品出荷額 "
        plt.xlabel("Year")
        plt.ylabel("Manufactured product shipment amount(Unit: 10,000 yen)")
        plt.legend()
        plt.grid(True)
        img = io.BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode("utf-8")
        return render_template(
            "index.html", image_data=img_base64, prefName=prefName, cityName=cityName, Title=Title
        )


if __name__ == "__main__":
    app.run(port=8000, debug=True)
