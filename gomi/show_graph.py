# import matplotlib
# import base64

# # import matplotlib.pyplot as plt
# from flask import Flask, render_template
# import io
# from gomi.kigyo_hukakachi import get_data
# import numpy as np
# from gomi.lsm import lsm

# app = Flask(__name__)
# matplotlib.use("Agg")


# # グラフを作成
# # @app.route("/2")
# # def show_graph():
# #     limited_years = [2012, 2016]
# #     data_list = get_data(limited_years)
# #     # メインスレッドでFigureを作成
# #     fig, ax = plt.subplots()
# #     ax.plot(limited_years, data_list)
# #     # 画像を保存し、Base64エンコード
# #     img = io.BytesIO()
# #     plt.savefig(img, format="png")
# #     img.seek(0)
# #     img_base64 = base64.b64encode(img.getvalue()).decode("utf-8")
# #     return render_template("index.html", image_data=img_base64)


# # @app.route("/")
# # def show_graph2():
# #     limited_years = [2012, 2016]
# #     # data_list = get_data(limited_years)
# #     y = np.array(data_list)  # NumPy配列に変換
# #     x = np.array(limited_years)
# #     plt = lsm(x, y)

# #     # 画像を保存し、Base64エンコード
# #     img = io.BytesIO()
# #     plt.savefig(img, format="png")
# #     img.seek(0)
# #     img_base64 = base64.b64encode(img.getvalue()).decode("utf-8")
# #     return render_template("index.html", image_data=img_base64)


# # def reg1dim(x, y):
# #     a = np.dot(x, y) / (x**2).sum()
# #     a = reg1dim(x, y)

# #     plt.scatter(x, y, color="k")
# #     plt.plot([0, x.max()], [0, a * x.max()])  # x.max() 配列xの最大値まで
# #     plt.show()


# if __name__ == "__main__":
#     app.run(port=8000, debug=True)
