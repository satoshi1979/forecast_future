import matplotlib
import base64
from pref_cities import get_city_code2
from flask import Flask, render_template, request
import io
import numpy as np
from lsm2 import forecast_and_plot_svr
import matplotlib.pyplot as plt

from functions import (
    wiki,
    get_data_fukakachi,
    seizou_syukka,
    population,
    retail_sells,
    asset_value,
    show_japan_map,
)

# 共通
api_key = "0iKaDKQrdMpKRS2LVhDifNC8QxMWDASPp9HVlnB7"
headers = {"X-API-KEY": api_key}

app = Flask(__name__)
matplotlib.use("Agg")


@app.route("/")
def top():
    return render_template("top.html")


# 付加価値額


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
        years = int(request.form["years"])
        prefCode, cityCode = get_city_code2(prefName, cityName)
        limited_years = [2012, 2016]
        data_list = get_data_fukakachi(prefCode, cityCode, limited_years)
        y = np.array(data_list)  # NumPy配列に変換
        x = np.array(limited_years)
        X_forecast, y_forecast = forecast_and_plot_svr(x, y, years)
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
        # Generate the map image and encode it in Base64
        pref_colors = {prefName: "Blue"}
        map_image_data = show_japan_map(pref_colors)
        Citywiki = wiki(cityName)
        return render_template(
            "index.html",
            image_data=img_base64,
            prefName=prefName,
            cityName=cityName,
            Title=Title,
            map=map_image_data,
            Citywiki=Citywiki,
        )


# 付加価値額ここまで
# 製造業出荷額


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
        forecast_years = int(request.form["years"])
        prefCode, cityCode = get_city_code2(prefName, cityName)
        data_list, years = seizou_syukka(prefCode, cityCode)
        y = np.array(data_list)  # NumPy配列に変換
        x = np.array(years)
        X_forecast, y_forecast = forecast_and_plot_svr(x, y, forecast_years)

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
        # Generate the map image and encode it in Base64
        pref_colors = {prefName: "Blue"}
        map_image_data = show_japan_map(pref_colors)
        Citywiki = wiki(cityName)
        return render_template(
            "index.html",
            image_data=img_base64,
            prefName=prefName,
            cityName=cityName,
            Title=Title,
            map=map_image_data,
            Citywiki=Citywiki,
        )


# 製造業出荷額ここまで
# 将来人口推計


@app.route("/population", methods=["GET", "POST"])
def show_population():
    if request.method == "GET":
        return render_template("index2.html")
    else:
        plt.clf()
        plt.close("all")
        prefName = request.form["prefName"]
        cityName = request.form["cityName"]
        forecast_years = int(request.form["years"])
        prefCode, cityCode = get_city_code2(prefName, cityName)
        data_list, years = population(prefCode, cityCode)
        y = np.array(data_list)  # NumPy配列に変換
        x = np.array(years)
        X_forecast, y_forecast = forecast_and_plot_svr(x, y, forecast_years)

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
        # Generate the map image and encode it in Base64
        pref_colors = {prefName: "Blue"}
        map_image_data = show_japan_map(pref_colors)
        Citywiki = wiki(cityName)
        return render_template(
            "index.html",
            image_data=img_base64,
            prefName=prefName,
            cityName=cityName,
            Title=Title,
            map=map_image_data,
            Citywiki=Citywiki,
        )


# 将来人口推計ここまで
# 年間商品販売額（百万円）


@app.route("/retail", methods=["GET", "POST"])
def show_retail():
    if request.method == "GET":
        return render_template("index2.html")
    else:
        plt.clf()
        plt.close("all")
        prefName = request.form["prefName"]
        cityName = request.form["cityName"]
        forecast_years = int(request.form["years"])
        prefCode, cityCode = get_city_code2(prefName, cityName)
        data_list, years = retail_sells(prefCode, cityCode)
        y = np.array(data_list)  # NumPy配列に変換
        x = np.array(years)
        X_forecast, y_forecast = forecast_and_plot_svr(x, y, forecast_years)

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
        # Generate the map image and encode it in Base64
        pref_colors = {prefName: "Blue"}
        map_image_data = show_japan_map(pref_colors)
        Citywiki = wiki(cityName)
        return render_template(
            "index.html",
            image_data=img_base64,
            prefName=prefName,
            cityName=cityName,
            Title=Title,
            map=map_image_data,
            Citywiki=Citywiki,
        )


# 年間商品販売額（百万円）ここまで
# 不動産取引価格


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
        forecast_years = int(request.form["years"])
        type = request.form["type"]
        prefCode, cityCode = get_city_code2(prefName, cityName)
        data_list = asset_value(prefCode, cityCode, type)
        y = np.array(data_list)  # NumPy配列に変換
        x = np.array(years)
        X_forecast, y_forecast = forecast_and_plot_svr(x, y, forecast_years)

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
        # Generate the map image and encode it in Base64
        pref_colors = {prefName: "Blue"}
        map_image_data = show_japan_map(pref_colors)
        Citywiki = wiki(cityName)
        return render_template(
            "index.html",
            image_data=img_base64,
            prefName=prefName,
            cityName=cityName,
            Title=Title,
            map=map_image_data,
            Citywiki=Citywiki,
        )


# 不動産取引価格ここまで
# 地図


if __name__ == "__main__":
    app.run(port=8000, debug=True)
