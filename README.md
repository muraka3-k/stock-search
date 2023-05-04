# stork-search

銘柄コードから株情報を取得する処理

- 銘柄コードと対象URLを指定する
- 銘柄ごとに対象ページへ遷移し、情報を取得する

# Install
```
git clone https://github.com/muraka3-k/stock-search.git
cd stock-search
pip install git+https://github.com/muraka3-k/stock-search.git
```

poetryをインストールしていない場合は以下のコマンドでインストールしてください。
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```
そして、環境に応じて、PoetryのPATHを通してください。

# ライブラリ

* jupyter notebook
* appium
* Beautiful Soup


# Run
## sample_web_driverの実行時
`app/sample_web_driver.py`の146,147行目の書き換えを行う
```
url="調査対象のHPのURL"
ticker_list=["銘柄コード", "銘柄コード"]
```

```
python app/sample_web_driver.py
```


# Run（jupyter版）
## sample_web_driverの実行時
1. 環境変数用のファイル生成(`sample-code.ipynb`)：

    ```
    url="調査対象のHPのURL"
    ticker_list=["銘柄コード", "銘柄コード"]
    ```

2. 実行する(`sample-code.ipynb`)：

    1で入力した情報を元に、すべてを実行する

# Author

* Github   [muraka3-k](https://github.com/muraka3-k)

