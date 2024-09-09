from wikipedia import wikipedia
import requests

api_key = "0iKaDKQrdMpKRS2LVhDifNC8QxMWDASPp9HVlnB7"
headers = {"X-API-KEY": api_key}


# def wiki(cityName):
#     wikipedia.set_lang("jp")

#     words = wikipedia.search(cityName, results=1)

#     if not words:
#         print("一致なし")
#     else:
#         # 検索ワードがヒットすれば要約を取得
#         line = str(wikipedia.summary(words[0]))
#         return line


def wiki(cityName):
    wikipedia.set_lang("jp")

    try:
        page = wikipedia.page(cityName)
        if page.pageid == -1:
            # Disambiguation case (pageid of -1 indicates disambiguation)
            line = "候補が複数あるか、一致するページが見つかりません。"
            return line
        else:
            summary = wikipedia.summary(cityName)
            return summary
    except wikipedia.PageError:
        # Page doesn't exist
        line = "候補が複数あるか、一致するページが見つかりません。"
        return line
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        line = "候補が複数あるか、一致するページが見つかりません。"
        return line


def get_data_fukakachi(prefCode, cityCode, y):
    limited_years = [2012, 2016]
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


if __name__ == "__main__":
    word = wiki("盛岡市")
    print(word)
