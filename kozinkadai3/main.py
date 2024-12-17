# ## 改良２
# import flet as ft  # Fletライブラリをインポート
# import requests    # HTTPリクエストを扱うrequestsライブラリをインポート

# # 気象庁のエリア情報APIのURL
# BASE_API_URL = "http://www.jma.go.jp/bosai/common/const/area.json"
# # 気象庁の天気予報APIのURL
# WEATHER_API_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/"

# def main(page: ft.Page):
#     # ページのタイトルとスクロール設定
#     page.title = "地域別天気予報アプリ"
#     page.scroll = "auto"

#     # 初期データの取得と処理
#     try:
#         response = requests.get(BASE_API_URL)  # エリア情報を取得
#         response.raise_for_status()            # リクエストが成功したか確認
#         data = response.json()                 # JSONデータを辞書型に変換

#         # 地方コードと名称の辞書を作成
#         regions = {code: info["name"] for code, info in data["centers"].items()}
#         # 気象台や事務所の情報を取得
#         offices = data["offices"]
#     except Exception as e:
#         # データ取得に失敗した場合、エラーメッセージを表示して終了
#         page.add(ft.Text(f"データの取得に失敗しました: {e}", color=ft.colors.RED))
#         return

#     # ウィジェットの定義
#     # 地方選択用のドロップダウンメニュー
#     region_dropdown = ft.Dropdown(
#         label="地方を選択",
#         # regionsの辞書からドロップダウンのオプションを作成
#         options=[ft.dropdown.Option(key, value) for key, value in regions.items()],
#         on_change=lambda e: update_offices(e.control.value),  # 選択変更時の処理
#     )
#     # 詳細地域選択用のドロップダウンメニュー（初期状態では無効）
#     office_dropdown = ft.Dropdown(label="詳細地域を選択", disabled=True, on_change=lambda e: fetch_weather(e.control.value))
#     # 天気予報の結果を表示するテキストフィールド
#     weather_output = ft.Text(expand=True)

#     # 地方選択後の詳細地域の更新処理
#     def update_offices(region_code):
#         office_dropdown.options.clear()  # 以前のオプションをクリア
#         office_dropdown.disabled = True  # 一時的に無効化
#         weather_output.value = ""        # 天気予報の表示をクリア
#         page.update()                    # ページを更新

#         if not region_code:
#             return  # 地方が選択されていない場合、処理を終了

#         # 選択された地域の詳細地域情報を取得
#         try:
#             region_data = data["centers"].get(region_code)
#             if region_data:
#                 # 詳細地域のドロップダウンオプションを作成
#                 office_dropdown.options = [
#                     ft.dropdown.Option(
#                         child,
#                         f"{offices[child]['name']} ({offices[child]['officeName']})"
#                     )
#                     for child in region_data["children"] if child in offices
#                 ]
#                 office_dropdown.disabled = False  # ドロップダウンを有効化
#         except Exception as e:
#             # エラーが発生した場合、エラーメッセージを表示
#             weather_output.value = f"詳細地域の取得に失敗しました: {e}"

#         page.update()  # ページを更新

#     # 天気予報を取得し、表示する処理
#     def fetch_weather(selected_code):
#         weather_output.value = ""  # 天気予報の表示をクリア
#         if not selected_code:
#             weather_output.value = "詳細地域を選択してください。"
#             page.update()
#             return  # 詳細地域が選択されていない場合、処理を終了

#         # 天気予報データの取得
#         try:
#             response = requests.get(f"{WEATHER_API_URL}{selected_code}.json")  # 選択された地域の天気予報を取得
#             response.raise_for_status()  # リクエストが成功したか確認
#             weather_data = response.json()  # JSONデータを辞書型に変換

#             # 地域ごとに情報をまとめるための辞書を用意
#             area_forecasts = {}

#             # 天気予報データ内の各エントリを処理
#             for weather_entry in weather_data:
#                 publishing_office = weather_entry["publishingOffice"]   # 発表機関
#                 report_datetime = weather_entry["reportDatetime"]       # 発表日時
#                 time_series = weather_entry["timeSeries"]               # 時間帯ごとの予報データ

#                 # timeSeriesごとの処理
#                 for ts in time_series:
#                     time_defines = ts["timeDefines"]  # 各予報の日時リスト
#                     areas = ts["areas"]               # 地域ごとの予報データ

#                     # 地域ごとの情報を処理
#                     for area in areas:
#                         area_name = area["area"]["name"]  # 地域名

#                         # 地域名で辞書にエントリがなければ作成
#                         if area_name not in area_forecasts:
#                             area_forecasts[area_name] = {
#                                 "publishingOffice": publishing_office,
#                                 "reportDatetime": report_datetime,
#                                 "forecasts": []
#                             }

#                         # 各種情報を取得し、表示用リストに追加
#                         for idx, time_define in enumerate(time_defines):
#                             forecast_text = f"日時: {time_define.replace('T', ' ').split('+')[0]}\n"

#                             if "weathers" in area:
#                                 weather = area["weathers"][idx] if idx < len(area["weathers"]) else "情報なし"
#                                 forecast_text += f"天気: {weather}\n"

#                             if "winds" in area:
#                                 wind = area["winds"][idx] if idx < len(area["winds"]) else "情報なし"
#                                 forecast_text += f"風: {wind}\n"

#                             if "waves" in area:
#                                 wave = area["waves"][idx] if idx < len(area["waves"]) else "情報なし"
#                                 forecast_text += f"波: {wave}\n"

#                             if "pops" in area:
#                                 pop = area["pops"][idx] if idx < len(area["pops"]) else "情報なし"
#                                 forecast_text += f"降水確率: {pop}%\n"

#                             if "temps" in area:
#                                 temp = area["temps"][idx] if idx < len(area["temps"]) else "情報なし"
#                                 forecast_text += f"気温: {temp}℃\n"

#                             if "tempsMax" in area:
#                                 temp_max = area["tempsMax"][idx] if idx < len(area["tempsMax"]) else "情報なし"
#                                 forecast_text += f"最高気温: {temp_max}℃\n"

#                             if "tempsMin" in area:
#                                 temp_min = area["tempsMin"][idx] if idx < len(area["tempsMin"]) else "情報なし"
#                                 forecast_text += f"最低気温: {temp_min}℃\n"

#                             if "reliabilities" in area:
#                                 reliability = area["reliabilities"][idx] if idx < len(area["reliabilities"]) else "情報なし"
#                                 forecast_text += f"信頼度: {reliability}\n"

#                             # 地域の予報リストに追加
#                             area_forecasts[area_name]["forecasts"].append(forecast_text)

#                 # 平均気温や降水量がある場合、それらの情報を地域ごとに追加
#                 if "tempAverage" in weather_entry:
#                     for avg_area in weather_entry["tempAverage"]["areas"]:
#                         area_name = avg_area["area"]["name"]  # 地域名

#                         if area_name not in area_forecasts:
#                             area_forecasts[area_name] = {
#                                 "publishingOffice": publishing_office,
#                                 "reportDatetime": report_datetime,
#                                 "forecasts": []
#                             }

#                         min_temp = avg_area.get("min", "情報なし")
#                         max_temp = avg_area.get("max", "情報なし")
#                         avg_forecast = f"\n■平均気温\n最低気温の平均: {min_temp}℃\n最高気温の平均: {max_temp}℃\n"
#                         area_forecasts[area_name]["forecasts"].append(avg_forecast)

#                 if "precipAverage" in weather_entry:
#                     for avg_area in weather_entry["precipAverage"]["areas"]:
#                         area_name = avg_area["area"]["name"]  # 地域名

#                         if area_name not in area_forecasts:
#                             area_forecasts[area_name] = {
#                                 "publishingOffice": publishing_office,
#                                 "reportDatetime": report_datetime,
#                                 "forecasts": []
#                             }

#                         min_precip = avg_area.get("min", "情報なし")
#                         max_precip = avg_area.get("max", "情報なし")
#                         precip_forecast = f"\n■平均降水量\n最少降水量: {min_precip}mm\n最多降水量: {max_precip}mm\n"
#                         area_forecasts[area_name]["forecasts"].append(precip_forecast)

#             # 地域ごとに情報をまとめて表示用文字列を構築
#             forecast_text = ""
#             for area_name, area_info in area_forecasts.items():
#                 forecast_text += f"\n=== 地域: {area_name} ===\n"
#                 forecast_text += f"発表機関: {area_info['publishingOffice']}\n発表日時: {area_info['reportDatetime']}\n"

#                 for forecast in area_info["forecasts"]:
#                     forecast_text += f"{forecast}\n"

#             # 表示用テキストを設定（データがない場合はメッセージを表示）
#             weather_output.value = forecast_text.strip() if forecast_text.strip() else "天気情報がありません。"

#         except Exception as e:
#             # 天気情報の取得に失敗した場合、エラーメッセージを表示
#             weather_output.value = f"天気情報の取得に失敗しました: {e}"

#         page.update()  # ページを更新

#     # ページにウィジェットを追加
#     page.add(
#         ft.Column(
#             [
#                 ft.Text("地域別天気予報アプリ", size=20, weight="bold"),  # タイトル
#                 region_dropdown,  # 地方選択ドロップダウン
#                 office_dropdown,  # 詳細地域選択ドロップダウン
#                 ft.Divider(),     # 区切り線
#                 ft.Text("天気予報:", size=16),  # 「天気予報:」のラベル
#                 weather_output,   # 天気予報の表示フィールド
#             ],
#             expand=True,
#         )
#     )

# # アプリの起動
# if __name__ == "__main__":
#     ft.app(target=main)

# ## 改良２


# ## 改良３

## 改良３
import flet as ft
import requests
import sqlite3
import os

# 気象庁のエリア情報APIのURL
BASE_API_URL = "http://www.jma.go.jp/bosai/common/const/area.json"
# 気象庁の天気予報APIのURL
WEATHER_API_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/"
# データベースファイルのパス
DB_FILE = "kozinkadai3/weather_data.db"

# データベースの初期化処理（main関数の外側に移動）
def init_database():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)  # データベースファイルを削除して再作成
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # テーブル作成
    # エリアテーブル
    cursor.execute(
        """
        CREATE TABLE areas (
            area_id INTEGER PRIMARY KEY AUTOINCREMENT,
            area_name TEXT UNIQUE
        )
        """
    )
    # 予報テーブル
    cursor.execute(
        """
        CREATE TABLE forecasts (
            forecast_id INTEGER PRIMARY KEY AUTOINCREMENT,
            area_id INTEGER,
            date_time TEXT,
            weather TEXT,
            wind TEXT,
            wave TEXT,
            pop TEXT,
            temp TEXT,
            temp_max TEXT,
            temp_min TEXT,
            FOREIGN KEY (area_id) REFERENCES areas(area_id)
        )
        """
    )
    # 平均情報テーブル
    cursor.execute(
        """
        CREATE TABLE averages (
            average_id INTEGER PRIMARY KEY AUTOINCREMENT,
            area_id INTEGER,
            avg_type TEXT,
            min_value TEXT,
            max_value TEXT,
            FOREIGN KEY (area_id) REFERENCES areas(area_id)
        )
        """
    )
    conn.commit()
    conn.close()

def main(page: ft.Page):
    page.title = "地域別天気予報アプリ"
    page.scroll = "auto"

    # データベースの初期化
    init_database()

    try:
        response = requests.get(BASE_API_URL)
        response.raise_for_status()
        data = response.json()

        # 地方コードと名称の辞書を作成
        regions = {code: info["name"] for code, info in data["centers"].items()}
        # 気象台や事務所の情報を取得
        offices = data["offices"]
    except Exception as e:
        page.add(ft.Text(f"データの取得に失敗しました: {e}", color=ft.colors.RED))
        return

    region_dropdown = ft.Dropdown(
        label="地方を選択",
        options=[ft.dropdown.Option(key, value) for key, value in regions.items()],
        on_change=lambda e: update_offices(e.control.value),
    )
    office_dropdown = ft.Dropdown(
        label="詳細地域を選択",
        disabled=True,
        on_change=lambda e: fetch_weather(e.control.value),
    )
    weather_output = ft.Text(expand=True)

    # 地方選択後の詳細地域の更新処理
    def update_offices(region_code):
        office_dropdown.options.clear()
        office_dropdown.disabled = True
        weather_output.value = ""
        page.update()

        if not region_code:
            return

        try:
            region_data = data["centers"].get(region_code)
            if region_data:
                office_dropdown.options = [
                    ft.dropdown.Option(
                        child,
                        f"{offices[child]['name']} ({offices[child]['officeName']})",
                    )
                    for child in region_data["children"]
                    if child in offices
                ]
                office_dropdown.disabled = False
        except Exception as e:
            weather_output.value = f"詳細地域の取得に失敗しました: {e}"

        page.update()

    # 地域名を正規化する関数（「地方」を削除）
    def normalize_area_name(name):
        return name.replace("地方", "").strip()

    # 天気予報を取得し、表示およびデータベースに保存する処理
    def fetch_weather(selected_code):
        weather_output.value = ""
        if not selected_code:
            weather_output.value = "詳細地域を選択してください。"
            page.update()
            return

        try:
            response = requests.get(f"{WEATHER_API_URL}{selected_code}.json")
            response.raise_for_status()
            weather_data = response.json()

            forecast_text = ""

            # エリアごとにデータを集約する辞書を作成
            area_data = {}

            # データベース接続
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()

            # 天気予報データ内の各エントリを処理
            for weather_entry in weather_data:
                time_series = weather_entry.get("timeSeries", [])

                # timeSeriesごとの処理
                for ts in time_series:
                    time_defines = ts["timeDefines"]
                    areas = ts["areas"]

                    # 地域ごとの情報を処理
                    for area in areas:
                        area_name = normalize_area_name(area["area"]["name"])

                        if area_name not in area_data:
                            area_data[area_name] = {
                                "forecasts": {},
                                "averages": [],
                                "has_weather_data": False,  # "天気" 情報の有無を追跡
                            }
                            # エリア情報をデータベースに保存
                            cursor.execute(
                                """
                                INSERT OR IGNORE INTO areas (area_name)
                                VALUES (?)
                                """,
                                (area_name,),
                            )
                            conn.commit()

                        # 各種情報を取得し、リストに追加
                        for idx, time_define in enumerate(time_defines):
                            data_exists = False
                            forecast = {}

                            # 各種情報の存在チェック関数
                            def add_info(key, label, unit=""):
                                nonlocal data_exists
                                if key in area:
                                    if idx < len(area[key]):
                                        value = area[key][idx]
                                        if value and value != "情報なし":
                                            forecast[label] = value + unit
                                            data_exists = True
                                            if label == "天気":
                                                # "天気" 情報がある場合、フラグをTrueに設定
                                                area_data[area_name]["has_weather_data"] = True

                            # 各種情報を追加
                            add_info("weathers", "天気")
                            add_info("winds", "風")
                            add_info("waves", "波")
                            add_info("pops", "降水確率", "%")
                            add_info("temps", "気温", "℃")
                            add_info("tempsMax", "最高気温", "℃")
                            add_info("tempsMin", "最低気温", "℃")

                            # いずれかのデータが存在する場合のみ追加
                            if data_exists:
                                date_time = time_define.replace("T", " ").split("+")[0]
                                date = date_time.split(" ")[0]  # 日付を取得
                                if date not in area_data[area_name]["forecasts"]:
                                    area_data[area_name]["forecasts"][date] = []
                                forecast_entry = f"■日時: {date_time}\n"
                                for key, val in forecast.items():
                                    forecast_entry += f"{key}: {val}\n"
                                area_data[area_name]["forecasts"][date].append(forecast_entry)

                                # データベースに予報データを保存
                                cursor.execute(
                                    """
                                    INSERT INTO forecasts (
                                        area_id, date_time, weather, wind, wave,
                                        pop, temp, temp_max, temp_min
                                    )
                                    VALUES (
                                        (SELECT area_id FROM areas WHERE area_name = ?),
                                        ?, ?, ?, ?, ?, ?, ?, ?
                                    )
                                    """,
                                    (
                                        area_name,
                                        date_time,
                                        forecast.get("天気"),
                                        forecast.get("風"),
                                        forecast.get("波"),
                                        forecast.get("降水確率"),
                                        forecast.get("気温"),
                                        forecast.get("最高気温"),
                                        forecast.get("最低気温"),
                                    ),
                                )
                                conn.commit()

                # 平均気温や降水量がある場合、それらの情報を追加
                if "tempAverage" in weather_entry:
                    for avg_area in weather_entry["tempAverage"]["areas"]:
                        area_name = normalize_area_name(avg_area["area"]["name"])
                        # "天気" 情報がない場合、その地域をスキップ
                        if area_name not in area_data:
                            continue
                        min_temp = avg_area.get("min")
                        max_temp = avg_area.get("max")
                        if (min_temp and min_temp != " ") or (max_temp and max_temp != " "):
                            avg_text = f"■平均気温\n"
                            if min_temp and min_temp != " ":
                                avg_text += f"最低気温の平均: {min_temp}℃\n"
                            if max_temp and max_temp != " ":
                                avg_text += f"最高気温の平均: {max_temp}℃\n"
                            area_data[area_name]["averages"].append(avg_text)
                            # データベースに平均気温を保存
                            cursor.execute(
                                """
                                INSERT INTO averages (
                                    area_id, avg_type, min_value, max_value
                                )
                                VALUES (
                                    (SELECT area_id FROM areas WHERE area_name = ?),
                                    'temperature', ?, ?
                                )
                                """,
                                (area_name, min_temp, max_temp),
                            )
                            conn.commit()

                if "precipAverage" in weather_entry:
                    for avg_area in weather_entry["precipAverage"]["areas"]:
                        area_name = normalize_area_name(avg_area["area"]["name"])
                        # "天気" 情報がない場合、その地域をスキップ
                        if area_name not in area_data:
                            continue
                        min_precip = avg_area.get("min")
                        max_precip = avg_area.get("max")
                        if (min_precip and min_precip != " ") or (max_precip and max_precip != " "):
                            avg_text = f"■平均降水量\n"
                            if min_precip and min_precip != " ":
                                avg_text += f"最少降水量: {min_precip}mm\n"
                            if max_precip and max_precip != " ":
                                avg_text += f"最多降水量: {max_precip}mm\n"
                            area_data[area_name]["averages"].append(avg_text)
                            # データベースに平均降水量を保存
                            cursor.execute(
                                """
                                INSERT INTO averages (
                                    area_id, avg_type, min_value, max_value
                                )
                                VALUES (
                                    (SELECT area_id FROM areas WHERE area_name = ?),
                                    'precipitation', ?, ?
                                )
                                """,
                                (area_name, min_precip, max_precip),
                            )
                            conn.commit()

            # "天気" 情報の有無に基づいて地域をフィルタリング
            filtered_area_data = {
                area_name: area_info
                for area_name, area_info in area_data.items()
                if area_info["has_weather_data"]
            }

            # 集約したデータを表示用文字列に追加
            for area_name, area_info in filtered_area_data.items():
                area_forecasts_exist = False
                area_forecasts = ""

                # 日付順に並べ替えて表示
                for date in sorted(area_info["forecasts"].keys()):
                    date_forecasts = area_info["forecasts"][date]
                    if date_forecasts:
                        area_forecasts_exist = True
                        area_forecasts += f"\n◆{date}\n"
                        for forecast in date_forecasts:
                            area_forecasts += forecast + "\n"

                # 予報データが存在する場合のみ表示
                if area_forecasts_exist:
                    forecast_text += f"【地域】: {area_name}\n"
                    forecast_text += area_forecasts

                    # 平均値を表示
                    if area_info["averages"]:
                        forecast_text += "\n■平均情報\n"
                        for avg in area_info["averages"]:
                            forecast_text += avg

                    forecast_text += "\n"

            # 表示用テキストを設定（データがない場合はメッセージを表示）
            weather_output.value = (
                forecast_text.strip() if forecast_text.strip() else "天気情報がありません。"
            )

            conn.close()

        except Exception as e:
            weather_output.value = f"天気情報の取得に失敗しました: {e}"

        page.update()

    # ページにウィジェットを追加
    page.add(
        ft.Column(
            [
                ft.Text("地域別天気予報アプリ", size=20, weight="bold"),
                region_dropdown,
                office_dropdown,
                ft.Divider(),
                ft.Text("天気予報:", size=16),
                weather_output,
            ],
            expand=True,
        )
    )


# アプリの起動
if __name__ == "__main__":
    ft.app(target=main)