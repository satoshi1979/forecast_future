import wikipedia


def wiki(cityName):
    wikipedia.set_lang("jp")

    words = wikipedia.search(cityName, results=1)

    if not words:
        print("一致なし")
    else:
        # 検索ワードがヒットすれば要約を取得
        line = str(wikipedia.summary(words[0]))
        return line


if __name__ == "__main__":
    word = wiki("盛岡市")
    print(word)
