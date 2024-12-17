# pandasライブラリをインポート
import pandas as pd

# CSVファイルを読み込む
data = pd.read_csv('python/L3_python/winequality-red.csv')

# 5行目から10行目を取得して表示
# pandasのデータフレームはインデックスが0から始まるため、loc[4:9]を指定
subset = data.iloc[4:10]  # 5行目から10行目に相当する範囲
print(subset)
