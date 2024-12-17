# ## 改良２
# import flet as ft
# import requests

# # 気象庁のエリア情報APIのURL
# BASE_API_URL = "http://www.jma.go.jp/bosai/common/const/area.json"
# # 気象庁の天気予報APIのURL
# WEATHER_API_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/"


# def main(page: ft.Page):
#     page.title = "地域別天気予報アプリ"
#     page.scroll = "auto"

#     try:
#         response = requests.get(BASE_API_URL)
#         response.raise_for_status()
#         data = response.json()

#         # 地方コードと名称の辞書を作成
#         regions = {code: info["name"] for code, info in data["centers"].items()}
#         # 気象台や事務所の情報を取得
#         offices = data["offices"]
#     except Exception as e:
#         page.add(ft.Text(f"データの取得に失敗しました: {e}", color=ft.colors.RED))
#         return

#     region_dropdown = ft.Dropdown(
#         label="地方を選択",
#         options=[ft.dropdown.Option(key, value) for key, value in regions.items()],
#         on_change=lambda e: update_offices(e.control.value),
#     )
#     office_dropdown = ft.Dropdown(
#         label="詳細地域を選択",
#         disabled=True,
#         on_change=lambda e: fetch_weather(e.control.value),
#     )
#     weather_output = ft.Text(expand=True)

#     # 地方選択後の詳細地域の更新処理
#     def update_offices(region_code):
#         office_dropdown.options.clear()
#         office_dropdown.disabled = True
#         weather_output.value = ""
#         page.update()

#         if not region_code:
#             return

#         try:
#             region_data = data["centers"].get(region_code)
#             if region_data:
#                 office_dropdown.options = [
#                     ft.dropdown.Option(
#                         child,
#                         f"{offices[child]['name']} ({offices[child]['officeName']})",
#                     )
#                     for child in region_data["children"]
#                     if child in offices
#                 ]
#                 office_dropdown.disabled = False
#         except Exception as e:
#             weather_output.value = f"詳細地域の取得に失敗しました: {e}"

#         page.update()

#     # 地域名を正規化する関数（「地方」を削除）
#     def normalize_area_name(name):
#         return name.replace("地方", "").strip()

#     # 天気予報を取得し、表示する処理
#     def fetch_weather(selected_code):
#         weather_output.value = ""
#         if not selected_code:
#             weather_output.value = "詳細地域を選択してください。"
#             page.update()
#             return

#         try:
#             response = requests.get(f"{WEATHER_API_URL}{selected_code}.json")
#             response.raise_for_status()
#             weather_data = response.json()

#             forecast_text = ""

#             # エリアごとにデータを集約する辞書を作成
#             area_data = {}

#             # 天気予報データ内の各エントリを処理
#             for weather_entry in weather_data:
#                 time_series = weather_entry.get("timeSeries", [])

#                 # timeSeriesごとの処理
#                 for ts in time_series:
#                     time_defines = ts["timeDefines"]
#                     areas = ts["areas"]

#                     # 地域ごとの情報を処理
#                     for area in areas:
#                         area_name = normalize_area_name(area["area"]["name"])

#                         if area_name not in area_data:
#                             area_data[area_name] = {
#                                 "forecasts": {},
#                                 "averages": [],
#                                 "has_weather_data": False,  # "天気" 情報の有無を追跡
#                             }

#                         # 各種情報を取得し、リストに追加
#                         for idx, time_define in enumerate(time_defines):
#                             data_exists = False
#                             forecast = ""

#                             # 各種情報の存在チェック関数
#                             def add_info(key, label, unit=""):
#                                 nonlocal data_exists, forecast
#                                 if key in area:
#                                     if idx < len(area[key]):
#                                         value = area[key][idx]
#                                         if value and value != "情報なし":
#                                             forecast += f"{label}: {value}{unit}\n"
#                                             data_exists = True
#                                             if label == "天気":
#                                                 # "天気" 情報がある場合、フラグをTrueに設定
#                                                 area_data[area_name]["has_weather_data"] = True

#                             # 各種情報を追加
#                             add_info("weathers", "天気")
#                             add_info("winds", "風")
#                             add_info("waves", "波")
#                             add_info("pops", "降水確率", "%")
#                             add_info("temps", "気温", "℃")
#                             add_info("tempsMax", "最高気温", "℃")
#                             add_info("tempsMin", "最低気温", "℃")

#                             # いずれかのデータが存在する場合のみ追加
#                             if data_exists:
#                                 date_time = time_define.replace("T", " ").split("+")[0]
#                                 date = date_time.split(" ")[0]  # 日付を取得
#                                 if date not in area_data[area_name]["forecasts"]:
#                                     area_data[area_name]["forecasts"][date] = []
#                                 forecast_entry = f"■日時: {date_time}\n{forecast}"
#                                 area_data[area_name]["forecasts"][date].append(
#                                     forecast_entry
#                                 )

#                 # 平均気温や降水量がある場合、それらの情報を追加
#                 if "tempAverage" in weather_entry:
#                     for avg_area in weather_entry["tempAverage"]["areas"]:
#                         area_name = normalize_area_name(avg_area["area"]["name"])
#                         # "天気" 情報がない場合、その地域をスキップ
#                         if area_name not in area_data:
#                             continue
#                         min_temp = avg_area.get("min")
#                         max_temp = avg_area.get("max")
#                         if (min_temp and min_temp != " ") or (max_temp and max_temp != " "):
#                             avg_text = f"■平均気温\n"
#                             if min_temp and min_temp != " ":
#                                 avg_text += f"最低気温の平均: {min_temp}℃\n"
#                             if max_temp and max_temp != " ":
#                                 avg_text += f"最高気温の平均: {max_temp}℃\n"
#                             area_data[area_name]["averages"].append(avg_text)

#                 if "precipAverage" in weather_entry:
#                     for avg_area in weather_entry["precipAverage"]["areas"]:
#                         area_name = normalize_area_name(avg_area["area"]["name"])
#                         # "天気" 情報がない場合、その地域をスキップ
#                         if area_name not in area_data:
#                             continue
#                         min_precip = avg_area.get("min")
#                         max_precip = avg_area.get("max")
#                         if (min_precip and min_precip != " ") or (max_precip and max_precip != " "):
#                             avg_text = f"■平均降水量\n"
#                             if min_precip and min_precip != " ":
#                                 avg_text += f"最少降水量: {min_precip}mm\n"
#                             if max_precip and max_precip != " ":
#                                 avg_text += f"最多降水量: {max_precip}mm\n"
#                             area_data[area_name]["averages"].append(avg_text)

#             # "天気" 情報の有無に基づいて地域をフィルタリング
#             filtered_area_data = {
#                 area_name: area_info
#                 for area_name, area_info in area_data.items()
#                 if area_info["has_weather_data"]
#             }

#             # 集約したデータを表示用文字列に追加
#             for area_name, area_info in filtered_area_data.items():
#                 area_forecasts_exist = False
#                 area_forecasts = ""

#                 # 日付順に並べ替えて表示
#                 for date in sorted(area_info["forecasts"].keys()):
#                     date_forecasts = area_info["forecasts"][date]
#                     if date_forecasts:
#                         area_forecasts_exist = True
#                         area_forecasts += f"\n◆{date}\n"
#                         for forecast in date_forecasts:
#                             area_forecasts += forecast + "\n"

#                 # 予報データが存在する場合のみ表示
#                 if area_forecasts_exist:
#                     forecast_text += f"【地域】: {area_name}\n"
#                     forecast_text += area_forecasts

#                     # 平均値を表示
#                     if area_info["averages"]:
#                         forecast_text += "\n■平均情報\n"
#                         for avg in area_info["averages"]:
#                             forecast_text += avg

#                     forecast_text += "\n"

#             # 表示用テキストを設定（データがない場合はメッセージを表示）
#             weather_output.value = (
#                 forecast_text.strip() if forecast_text.strip() else "天気情報がありません。"
#             )

#         except Exception as e:
#             weather_output.value = f"天気情報の取得に失敗しました: {e}"

#         page.update()

#     # ページにウィジェットを追加
#     page.add(
#         ft.Column(
#             [
#                 ft.Text("地域別天気予報アプリ", size=20, weight="bold"),
#                 region_dropdown,
#                 office_dropdown,
#                 ft.Divider(),
#                 ft.Text("天気予報:", size=16),
#                 weather_output,
#             ],
#             expand=True,
#         )
#     )


# # アプリの起動
# if __name__ == "__main__":
#     ft.app(target=main)



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