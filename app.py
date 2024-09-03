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


# 製造業出荷額ここまで
# 将来人口推計


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


@app.route("/population", methods=["GET", "POST"])
def show_population():
    if request.method == "GET":
        return render_template("index2.html")
    else:
        plt.clf()
        plt.close("all")
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
        Title = "将来人口推計"
        plt.legend()
        plt.grid(True)

        img = io.BytesIO()
        plt.savefig(img, format="png")
        plt.close()  # メモリリークを防ぐためにfigureを閉じる
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode("utf-8")
        return render_template(
            "index.html", image_data=img_base64, prefName=prefName, cityName=cityName, Title=Title
        )


# 将来人口推計ここまで
# 年間商品販売額（百万円）


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


@app.route("/retail", methods=["GET", "POST"])
def show_retail():
    if request.method == "GET":
        return render_template("index2.html")
    else:
        plt.clf()
        plt.close("all")
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
        plt.ylabel("Annual product sales (Unit: million yen)")
        Title = "年間商品販売額"
        plt.legend()
        plt.grid(True)
        img = io.BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode("utf-8")
        return render_template(
            "index.html", image_data=img_base64, prefName=prefName, cityName=cityName, Title=Title
        )


# 年間商品販売額（百万円）ここまで
# 不動産取引価格


def asset_value(prefCode, cityCode, type):

    data_list = []
    years = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
    for year in years:
        base_url = "https://opendata.resas-portal.go.jp/api/v1/townPlanning/estateTransaction/bar?"
        params = f"year={year}&prefCode={prefCode}&cityCode={cityCode}&displayType={type}"
        url = base_url + params
        response = requests.get(url, headers=headers)
        data = response.json()
        if data["result"] is not None and "result" in data:
            result = data["result"]  # result に代入
            if "years" in result and len(result["years"]) > 0:
                value = result["years"][0]["value"]
                if value is not None:
                    data_list.append(value)
        else:
            data_list.append(0)  # 値がNoneの場合、0を追加
    return data_list


# https://qiita.com/Sei123/items/b825abae8ba6cf3eb0ff, methods=["GET", "POST"]


@app.route("/estate", methods=["GET", "POST"])
def estate():
    if request.method == "GET":
        return render_template("index3.html")
    else:
        plt.clf()
        plt.close("all")
        years = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
        prefName = request.form["prefName"]
        cityName = request.form["cityName"]
        type = request.form["type"]
        prefCode, cityCode = get_city_code2(prefName, cityName)
        data_list = asset_value(prefCode, cityCode, type)
        y = np.array(data_list)  # NumPy配列に変換
        x = np.array(years)
        X_forecast, y_forecast = forecast_and_plot_svr(x, y)

        # プロットを作成
        plt.figure(figsize=(12, 6))
        plt.scatter(x, y, color="darkorange", label="Actual data")
        plt.plot(X_forecast, y_forecast, color="navy", label="SVR prediction")
        plt.xlabel("Year")
        plt.ylabel("Real estate transaction price (average price per area)")
        Title = "不動産取引価格(面積あたり平均価格)"
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


if __name__ == "__main__":
    app.run(port=8000, debug=True)
