# stork-search

## 銘柄コードから株情報を取得する処理

- 銘柄コードと対象URLを指定する
- 銘柄ごとに対象ページへ遷移し、情報を取得する

## ツール

* jupyter notebook
* appium `pip install selenium`
* Beautiful Soup `pip install beautifulsoup4`

### 実行手順
1. 環境変数用のファイル生成(`sample-code.ipynb`)：

    ```
    url="調査対象のHPのURL"
    ticker_list=["銘柄コード", "銘柄コード"]
    ```

2. 実行する(`sample-code.ipynb`)：

    1で入力した情報を元に、すべてを実行する

