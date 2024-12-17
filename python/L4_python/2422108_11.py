import pandas as pd

# 各CSVデータをファイルパスからデータフレームに読み込む
users = pd.read_csv('python/L4_python/users.csv')
orders = pd.read_csv('python/L4_python/orders.csv')
items = pd.read_csv('python/L4_python/items.csv')

# 注文データと商品データを結合し、注文ごとの購入金額を計算する
merged_data = pd.merge(orders, items, on='item_id')
merged_data['purchase_amount'] = merged_data['order_num'] * merged_data['item_price']

# 各ユーザごとの平均購入金額を計算
average_purchase_per_user = merged_data.groupby('user_id')['purchase_amount'].mean().reset_index()

# 最も高い平均購入金額を取得
max_average_purchase = average_purchase_per_user.loc[average_purchase_per_user['purchase_amount'].idxmax()]

# 指定された形式で出力（np.float64を標準float型に変換）
print([int(max_average_purchase['user_id']), float(max_average_purchase['purchase_amount'])])
