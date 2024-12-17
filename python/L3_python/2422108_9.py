# pandasライブラリをインポート
import pandas as pd

# CSVファイルをデータフレームとして読み込む
data = pd.read_csv('python/L3_python/winequality-red.csv')

# "quality"の値ごとに平均値を計算
# groupby()で"quality"列を基準にグループ化し、mean()で各列の平均を計算
quality_means = data.groupby('quality').mean()

# 結果を表示
print(quality_means)
