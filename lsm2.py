import numpy as np
import pandas as pd
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler


def forecast_and_plot_svr(x, y, forecast_years):
    # データの準備
    X = x.reshape(-1, 1)
    y = y.reshape(-1, 1)

    # スケーリング
    scaler_X = StandardScaler()
    scaler_y = StandardScaler()
    X_scaled = scaler_X.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y)

    # SVRモデルの訓練
    svr_rbf = SVR(kernel="rbf", C=1, gamma=0.1, epsilon=0.1)
    svr_rbf.fit(X_scaled, y_scaled.ravel())

    # 予測用のデータ作成
    X_forecast = np.arange(min(x), max(x) + forecast_years, 1).reshape(-1, 1)
    X_forecast_scaled = scaler_X.transform(X_forecast)

    # 予測
    y_forecast_scaled = svr_rbf.predict(X_forecast_scaled)
    y_forecast = scaler_y.inverse_transform(y_forecast_scaled.reshape(-1, 1))

    return X_forecast, y_forecast


if __name__ == "__main__":

    # 使用例
    x = np.array([2012, 2016, 2027, 2040])
    y = np.array([333, 4646, 5655, 353])
    X_forecast, y_forecast = forecast_and_plot_svr(x, y, forecast_years=30)

    # 予測結果の表示
    forecast_df = pd.DataFrame({"Year": X_forecast.ravel(), "Predicted Value": y_forecast.ravel()})
    print(forecast_df)
