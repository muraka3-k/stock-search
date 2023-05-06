# stork-search

銘柄コードから株情報を取得する処理

- 銘柄コードと対象URLを指定する
- 銘柄ごとに対象ページへ遷移し、情報を取得する

# インストール手順
```
git clone https://github.com/muraka3-k/stock-search.git
cd stock-search
poetry install
```

poetryをインストールしていない場合は以下のコマンドでインストールしてください。
```
curl -sSL https://install.python-poetry.org | python3 -
```
そして、環境に応じて、PoetryのPATHを通してください。

# 使用ライブラリ

* jupyter notebook
* appium
* Beautiful Soup
* lxml

手動でインストールする場合は、以下のコマンドを使用してください。
```
pip install jupyter
pip install selenium
pip install chromedriver-binary-auto
pip install beautifulsoup4
pip install lxml
```

# Run
## kabutan_web_driverの実行時

### 直接指定する場合

```
poetry shell
python app/kabutane_web_driver.py 2914 9104 9433
```

### ファイル内で指定する場合
`app/kabutane_web_driver.py`の215行目の書き換えを行う

呼び出し時に銘柄コードを指定した場合は、その入力を優先します

``` diff python
- ticker_list = [2914, 9104]
+ ticker_list=["銘柄コード", "銘柄コード"]
```

```
poetry shell
python app/kabutan_web_driver.py
```

## sample_web_driverの実行時

### 直接指定する場合

```
poetry shell
python app/sample_web_driver.py 2914 9104 9433
```

### ファイル内で指定する場合
`app/sample_web_driver.py`の150行目と153行目の書き換えを行う
``` diff python
- ticker_list = [2914, 9104]
+ ticker_list=["銘柄コード", "銘柄コード"]

- url = ""
+ url = "指定サイトのURL"
```


```
poetry shell
python app/sample_web_driver.py

### 直接設定時はスペースで区切る
python app/sample_web_driver.py 2914 9104 9433
```


# Run（jupyter版）
## kabutanによる情報抽出の実行時
1. jupyterを立ち上げる
```
poetry shell
jupyter noootbook
```
2. 環境変数用のファイル生成(`kabutan.ipynb`)：

    ```
    ticker_list=["銘柄コード", "銘柄コード"]  ## （例）[2914, 9104, 9433]
    ```

3. 実行する(`kabutan.ipynb`)：

    1で入力した情報を元に、すべてを実行する

## sample_web_driverの実行時
1. jupyterを立ち上げる
```
poetry shell
jupyter noootbook
```
2. 環境変数用のファイル生成(`sample-code.ipynb`)：

    ```
    url="調査対象のHPのURL"
    ticker_list=["銘柄コード", "銘柄コード"]
    ```

3. 実行する(`sample-code.ipynb`)：

    1で入力した情報を元に、すべてを実行する

#　注意事項
- 銘柄コードのチェック等を一切行っていないため、文字列/存在しない銘柄コード等の入力時に検索できません

# Author

* Github   [muraka3-k](https://github.com/muraka3-k)

