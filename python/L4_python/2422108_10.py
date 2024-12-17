import pandas as pd

# 各CSVデータをファイルパスからデータフレームに読み込む
users = pd.read_csv('python/L4_python/users.csv')
orders = pd.read_csv('python/L4_python/orders.csv')
items = pd.read_csv('python/L4_python/items.csv')

# 注文データと商品データを結合し、注文ごとの購入金額を計算する
merged_data = pd.merge(orders, items, on='item_id')
merged_data['purchase_amount'] = merged_data['order_num'] * merged_data['item_price']

# 最も高い購入金額を取得
max_purchase = merged_data.loc[merged_data['purchase_amount'].idxmax()]

# 指定された形式で出力（np.int64を標準int型に変換）
print([int(max_purchase['order_id']), int(max_purchase['purchase_amount'])])
