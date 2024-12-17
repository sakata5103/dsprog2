import pandas as pd  # pandasライブラリをインポート

# データファイルのパスを指定
users_path = "python/L4_python/users.csv"    # ユーザーデータのCSVファイルパス
orders_path = "python/L4_python/orders.csv"  # 注文データのCSVファイルパス
items_path = "python/L4_python/items.csv"    # 商品データのCSVファイルパス

# CSVファイルを読み込み、DataFrameとして格納
users_df = pd.read_csv(users_path)      # ユーザーデータを読み込む
orders_df = pd.read_csv(orders_path)    # 注文データを読み込む
items_df = pd.read_csv(items_path)      # 商品データを読み込む

# 推薦対象となる商品IDを指定
target_item_id = 101  # おすすめを行う基準となる商品ID

# 対象商品の情報を取得
target_item = items_df[items_df['item_id'] == target_item_id].iloc[0]  # 商品IDがtarget_item_idの商品の情報を取得
target_small_category = target_item['small_category']  # 対象商品の小カテゴリを取得
target_big_category = target_item['big_category']      # 対象商品の大カテゴリを取得
target_price = target_item['item_price']               # 対象商品の価格を取得
target_page_num = target_item['pages']                 # 対象商品のページ数を取得

# 対象商品以外の商品を候補としてフィルタリング
candidate_items = items_df[items_df['item_id'] != target_item_id].copy()  # 対象商品以外の商品を新たにDataFrameとしてコピー

# スコアリング関数を定義
def calculate_scores(row):
    # 小カテゴリが同じ場合はスコア0、異なる場合は1
    small_category_score = 0 if row['small_category'] == target_small_category else 1
    # 大カテゴリが同じ場合はスコア0、異なる場合は1
    big_category_score = 0 if row['big_category'] == target_big_category else 1
    # 価格差の絶対値を計算
    price_difference = abs(row['item_price'] - target_price)
    # ページ数差の絶対値を計算
    page_difference = abs(row['pages'] - target_page_num)

    # 各スコアをSeriesとして返す
    return pd.Series({
        'small_category_score': small_category_score,
        'big_category_score': big_category_score,
        'price_difference': price_difference,
        'page_difference': page_difference
    })

# スコアを計算し、DataFrameに新しい列として追加
candidate_items[['small_category_score', 'big_category_score', 'price_difference', 'page_difference']] = candidate_items.apply(calculate_scores, axis=1)

# スコアリング関数の1のスコアが0のものだけを選択（小カテゴリが同じ）
candidate_items_filtered = candidate_items[candidate_items['small_category_score'] == 0]

# さらに、2のスコアが0のものを選択（大カテゴリが同じ）
candidate_items_filtered = candidate_items_filtered[candidate_items_filtered['big_category_score'] == 0]

# 価格差の少ない順に並べ替え、価格差が同じ場合はページ数差が小さい順に並べ替え
candidate_items_filtered = candidate_items_filtered.sort_values(by=['price_difference', 'page_difference'])

# 推薦候補の上位3件を取得
recommendations = candidate_items_filtered.head(3)['item_id'].tolist()

# 結果を出力
print(recommendations)