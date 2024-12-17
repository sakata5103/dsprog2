# pandasライブラリをインポート
import pandas as pd

# CSVファイルをデータフレームとして読み込む
data = pd.read_csv('python/L3_python/winequality-red.csv')

# "quality"列が6以上の行をフィルタリング
filtered_data = data[data['quality'] >= 6]

# フィルタリングしたデータを"quality"の降順でソート
sorted_data = filtered_data.sort_values(by='quality', ascending=False)

# 結果を表示
print(sorted_data)
