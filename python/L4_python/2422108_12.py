import pandas as pd

# ファイルの読み込み
users_path = "python/L4_python/users.csv"
orders_path = "python/L4_python/orders.csv"
items_path = "python/L4_python/items.csv"

users_df = pd.read_csv(users_path)
orders_df = pd.read_csv(orders_path)
items_df = pd.read_csv(items_path)

# 推薦対象の商品ID
target_item_id = 101

# 対象商品の情報を取得
target_item = items_df[items_df['item_id'] == target_item_id].iloc[0]
target_small_category = target_item['small_category']
target_big_category = target_item['big_category']
target_price = target_item['item_price']
target_page_num = target_item['pages']

# 対象商品以外の商品をフィルタリング
candidate_items = items_df[items_df['item_id'] != target_item_id].copy()

# ルールに基づくスコアリング関数
def calculate_score(row):
    small_category_score = 0 if row['small_category'] == target_small_category else 1
    big_category_score = 0 if row['big_category'] == target_big_category else 1
    price_difference = abs(row['item_price'] - target_price)
    page_difference = abs(row['pages'] - target_page_num)

    # スコアは小カテゴリ、大カテゴリ、価格差、ページ数差の順で並べる
    return (small_category_score, big_category_score, price_difference, page_difference)

# スコア計算とソート
candidate_items['score'] = candidate_items.apply(calculate_score, axis=1)
candidate_items = candidate_items.sort_values(by='score')

# 推薦候補の上位3件を取得
recommendations = candidate_items.head(3)['item_id'].tolist()

# 結果の出力
print(recommendations)
