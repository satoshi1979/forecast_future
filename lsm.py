import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression


# 単回帰分析（例として最小二乗法）
# ここでは、scikit-learnのLinearRegressionを使用
def lsm(x, y):
    
    model = LinearRegression()
    model.fit(x.reshape(-1, 1), y)
    # 回帰係数と切片
    a = model.coef_[0]
    b = model.intercept_

    # プロット範囲の設定
    x_plot = np.linspace(x.min(), x.max() * 1.01, 100)
    y_plot = a * x_plot + b

    # プロット
    plt.plot(x_plot, y_plot)
    plt.scatter(x, y)
    plt.xlabel("年")
    plt.ylabel("y")
    plt.grid(True)

    # テキストの表示（データの範囲に合わせて調整）
    plt.text(
        x.min() + 3 * (x.max() - x.min()),
        y.min() + 0.9 * (y.max() - y.min()),
        "y = {:.2f}x + {:.2f}".format(a, b),
    )

    return plt


if __name__ == "__main__":
    # データ
    y = np.array([333, 4646])  # NumPy配列に変換
    x = np.array([2012, 2016])
    plot = lsm(x, y)
    print(plot)
    plt.show()
