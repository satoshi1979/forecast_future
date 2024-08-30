import matplotlib
import base64
from pref_cities import get_city_code2

# import matplotlib.pyplot as plt
from flask import Flask, render_template, request
import io
from kigyo_hukakachi import get_data2
import numpy as np
from lsm import lsm

app = Flask(__name__)
matplotlib.use("Agg")


def make_graph():
    prefName = request.form["prefName"]
    cityName = request.form["cityName"]
    prefCode, cityCode = get_city_code2(prefName, cityName)
    limited_years = [2012, 2016]
    data_list = get_data2(prefCode, cityCode, limited_years)
    y = np.array(data_list)  # NumPy配列に変換
    x = np.array(limited_years)
    plt = lsm(x, y)
    # 画像を保存し、Base64エンコード
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode("utf-8")
    return img_base64


@app.route("/", methods=["GET", "POST"])
def show_graph2():
    if request.method == "GET":
        # img_base64 = make_graph()
        return render_template("index2.html")
    else:
        prefName = request.form["prefName"]
        cityName = request.form["cityName"]
        prefCode, cityCode = get_city_code2(prefName, cityName)
        limited_years = [2012, 2016]
        data_list = get_data2(prefCode, cityCode, limited_years)
        y = np.array(data_list)  # NumPy配列に変換
        x = np.array(limited_years)
        plt = lsm(x, y)
        # 画像を保存し、Base64エンコード
        img = io.BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode("utf-8")
        return render_template("index.html", image_data=img_base64)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
