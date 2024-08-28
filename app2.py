import matplotlib
import base64
import matplotlib.pyplot as plt
from flask import Flask, render_template
import io
from kigyo_hukakachi import get_data

app = Flask(__name__)
limited_years = [2012, 2016]
matplotlib.use("Agg")


@app.route("/")
def show_graph():
    data_list = get_data()

    # メインスレッドでFigureを作成
    fig, ax = plt.subplots()
    ax.plot(limited_years, data_list)

    # 画像を保存し、Base64エンコード
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode("utf-8")

    return render_template("index.html", image_data=img_base64)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
