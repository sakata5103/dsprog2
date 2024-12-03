###10 完成でもいい3
# import flet as ft
# import requests

# BASE_API_URL = "http://www.jma.go.jp/bosai/common/const/area.json"
# WEATHER_API_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/"

# def main(page: ft.Page):
#     # ページ設定
#     page.title = "地域別天気予報アプリ"
#     page.scroll = "auto"

#     # 初期データ取得
#     try:
#         response = requests.get(BASE_API_URL)
#         response.raise_for_status()
#         data = response.json()
#         regions = {code: info["name"] for code, info in data["centers"].items()}
#         offices = data["offices"]
#     except Exception as e:
#         page.add(ft.Text(f"データの取得に失敗しました: {e}", color=ft.colors.RED))
#         return

#     # ウィジェットの定義
#     region_dropdown = ft.Dropdown(
#         label="地方を選択",
#         options=[ft.dropdown.Option(key, value) for key, value in regions.items()],
#         on_change=lambda e: update_offices(e.control.value),
#     )
#     office_dropdown = ft.Dropdown(label="詳細地域を選択", disabled=True, on_change=lambda e: fetch_weather(e.control.value))
#     weather_output = ft.Text(expand=True)

#     # 地方選択後の更新処理
#     def update_offices(region_code):
#         office_dropdown.options.clear()
#         office_dropdown.disabled = True
#         weather_output.value = ""
#         page.update()

#         if not region_code:
#             return

#         # 地方コードに基づく詳細地域を取得
#         try:
#             region_data = data["centers"].get(region_code)
#             if region_data:
#                 office_dropdown.options = [
#                     ft.dropdown.Option(
#                         child,
#                         f"{offices[child]['name']} ({offices[child]['officeName']})"
#                     )
#                     for child in region_data["children"] if child in offices
#                 ]
#                 office_dropdown.disabled = False
#         except Exception as e:
#             weather_output.value = f"詳細地域の取得に失敗しました: {e}"

#         page.update()

#     # 天気予報を取得して表示
#     def fetch_weather(selected_code):
#         weather_output.value = ""
#         if not selected_code:
#             weather_output.value = "詳細地域を選択してください。"
#             page.update()
#             return

#         # 天気情報を取得
#         try:
#             response = requests.get(f"{WEATHER_API_URL}{selected_code}.json")
#             response.raise_for_status()
#             weather_data = response.json()

#             # 必要な情報を抽出
#             latest_weather = weather_data[0]  # 最初の要素が最新のデータ
#             publishing_office = latest_weather["publishingOffice"]
#             report_datetime = latest_weather["reportDatetime"]
#             time_series = latest_weather["timeSeries"]

#             # 表示用の文字列を作成
#             forecast_text = f"発表機関: {publishing_office}\n発表日時: {report_datetime}\n\n"

#             for series in time_series:
#                 time_defines = series["timeDefines"]
#                 for area in series["areas"]:
#                     # 天気情報が存在するエリアのみ取得
#                     if "weathers" in area:
#                         forecast_text += f"地域: {area['area']['name']}\n"
#                         for time, weather, wind in zip(
#                             time_defines,
#                             area.get("weathers", []),
#                             area.get("winds", []),
#                         ):
#                             forecast_text += f"\n    日付: {time}\n    天気: {weather}\n    風: {wind}\n"

#                         forecast_text += "\n"

#             weather_output.value = forecast_text if forecast_text.strip() else "天気情報がありません。"
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
##10


## 改良１
import flet as ft  # Fletライブラリをインポート
import requests    # HTTPリクエストを扱うrequestsライブラリをインポート

# 気象庁のエリア情報APIのURL
BASE_API_URL = "http://www.jma.go.jp/bosai/common/const/area.json"
# 気象庁の天気予報APIのURL
WEATHER_API_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/"

def main(page: ft.Page):
    # ページのタイトルとスクロール設定
    page.title = "地域別天気予報アプリ"
    page.scroll = "auto"

    # 初期データの取得と処理
    try:
        response = requests.get(BASE_API_URL)  # エリア情報を取得
        response.raise_for_status()            # リクエストが成功したか確認
        data = response.json()                 # JSONデータを辞書型に変換
        
        # 地方コードと名称の辞書を作成
        regions = {code: info["name"] for code, info in data["centers"].items()}
        # 気象台や事務所の情報を取得
        offices = data["offices"]
    except Exception as e:
        # データ取得に失敗した場合、エラーメッセージを表示して終了
        page.add(ft.Text(f"データの取得に失敗しました: {e}", color=ft.colors.RED))
        return

    # ウィジェットの定義
    # 地方選択用のドロップダウンメニュー
    region_dropdown = ft.Dropdown(
        label="地方を選択",
        # regionsの辞書からドロップダウンのオプションを作成
        options=[ft.dropdown.Option(key, value) for key, value in regions.items()],
        on_change=lambda e: update_offices(e.control.value),  # 選択変更時の処理
    )
    # 詳細地域選択用のドロップダウンメニュー（初期状態では無効）
    office_dropdown = ft.Dropdown(label="詳細地域を選択", disabled=True, on_change=lambda e: fetch_weather(e.control.value))
    # 天気予報の結果を表示するテキストフィールド
    weather_output = ft.Text(expand=True)

    # 地方選択後の詳細地域の更新処理
    def update_offices(region_code):
        office_dropdown.options.clear()  # 以前のオプションをクリア
        office_dropdown.disabled = True  # 一時的に無効化
        weather_output.value = ""        # 天気予報の表示をクリア
        page.update()                    # ページを更新

        if not region_code:
            return  # 地方が選択されていない場合、処理を終了

        # 選択された地域の詳細地域情報を取得
        try:
            region_data = data["centers"].get(region_code)
            if region_data:
                # 詳細地域のドロップダウンオプションを作成
                office_dropdown.options = [
                    ft.dropdown.Option(
                        child,
                        f"{offices[child]['name']} ({offices[child]['officeName']})"
                    )
                    for child in region_data["children"] if child in offices
                ]
                office_dropdown.disabled = False  # ドロップダウンを有効化
        except Exception as e:
            # エラーが発生した場合、エラーメッセージを表示
            weather_output.value = f"詳細地域の取得に失敗しました: {e}"

        page.update()  # ページを更新

    # 天気予報を取得し、表示する処理
    def fetch_weather(selected_code):
        weather_output.value = ""  # 天気予報の表示をクリア
        if not selected_code:
            weather_output.value = "詳細地域を選択してください。"
            page.update()
            return  # 詳細地域が選択されていない場合、処理を終了

        # 天気予報データの取得
        try:
            response = requests.get(f"{WEATHER_API_URL}{selected_code}.json")  # 選択された地域の天気予報を取得
            response.raise_for_status()  # リクエストが成功したか確認
            weather_data = response.json()  # JSONデータを辞書型に変換

            forecast_text = ""  # 表示用の文字列を初期化

            # 天気予報データ内の各エントリを処理
            for weather_entry in weather_data:
                publishing_office = weather_entry["publishingOffice"]   # 発表機関
                report_datetime = weather_entry["reportDatetime"]       # 発表日時
                time_series = weather_entry["timeSeries"]               # 時間帯ごとの予報データ

                # 発表機関と日時を表示用文字列に追加
                forecast_text += f"発表機関: {publishing_office}\n発表日時: {report_datetime}\n"

                # timeSeriesごとの処理
                for ts in time_series:
                    time_defines = ts["timeDefines"]  # 各予報の日時リスト
                    areas = ts["areas"]               # 地域ごとの予報データ

                    # 地域ごとの情報を処理
                    for area in areas:
                        area_name = area["area"]["name"]  # 地域名
                        forecast_text += f"\n地域: {area_name}\n"

                        # 各種情報を取得し、表示用文字列に追加
                        for idx, time_define in enumerate(time_defines):
                            # 日時の形式を整形
                            date_time = time_define.replace("T", " ").split("+")[0]

                            forecast_text += f"\n日時: {date_time}\n"

                            # 天気情報を追加
                            if "weathers" in area:
                                # インデックスが範囲内か確認してデータを取得
                                weather = area["weathers"][idx] if idx < len(area["weathers"]) else "情報なし"
                                forecast_text += f"天気: {weather}\n"

                            # 風情報を追加
                            if "winds" in area:
                                wind = area["winds"][idx] if idx < len(area["winds"]) else "情報なし"
                                forecast_text += f"風: {wind}\n"

                            # 波情報を追加
                            if "waves" in area:
                                wave = area["waves"][idx] if idx < len(area["waves"]) else "情報なし"
                                forecast_text += f"波: {wave}\n"

                            # 降水確率を追加
                            if "pops" in area:
                                pop = area["pops"][idx] if idx < len(area["pops"]) else "情報なし"
                                forecast_text += f"降水確率: {pop}%\n"

                            # 気温を追加
                            if "temps" in area:
                                temp = area["temps"][idx] if idx < len(area["temps"]) else "情報なし"
                                forecast_text += f"気温: {temp}℃\n"

                            # 最高気温を追加
                            if "tempsMax" in area:
                                temp_max = area["tempsMax"][idx] if idx < len(area["tempsMax"]) else "情報なし"
                                forecast_text += f"最高気温: {temp_max}℃\n"

                            # 最低気温を追加
                            if "tempsMin" in area:
                                temp_min = area["tempsMin"][idx] if idx < len(area["tempsMin"]) else "情報なし"
                                forecast_text += f"最低気温: {temp_min}℃\n"

                            # 信頼度を追加
                            if "reliabilities" in area:
                                reliability = area["reliabilities"][idx] if idx < len(area["reliabilities"]) else "情報なし"
                                forecast_text += f"信頼度: {reliability}\n"

                # 平均気温や降水量がある場合、それらの情報を追加
                if "tempAverage" in weather_entry:
                    forecast_text += "\n■平均気温\n"
                    for avg_area in weather_entry["tempAverage"]["areas"]:
                        area_name = avg_area["area"]["name"]  # 地域名
                        min_temp = avg_area.get("min", "情報なし")  # 最低気温の平均
                        max_temp = avg_area.get("max", "情報なし")  # 最高気温の平均
                        forecast_text += f"地域: {area_name}\n最低気温の平均: {min_temp}℃\n最高気温の平均: {max_temp}℃\n"

                if "precipAverage" in weather_entry:
                    forecast_text += "\n■平均降水量\n"
                    for avg_area in weather_entry["precipAverage"]["areas"]:
                        area_name = avg_area["area"]["name"]  # 地域名
                        min_precip = avg_area.get("min", "情報なし")  # 最少降水量
                        max_precip = avg_area.get("max", "情報なし")  # 最多降水量
                        forecast_text += f"地域: {area_name}\n最少降水量: {min_precip}mm\n最多降水量: {max_precip}mm\n"

            # 表示用テキストを設定（データがない場合はメッセージを表示）
            weather_output.value = forecast_text.strip() if forecast_text.strip() else "天気情報がありません。"

        except Exception as e:
            # 天気情報の取得に失敗した場合、エラーメッセージを表示
            weather_output.value = f"天気情報の取得に失敗しました: {e}"

        page.update()  # ページを更新

    # ページにウィジェットを追加
    page.add(
        ft.Column(
            [
                ft.Text("地域別天気予報アプリ", size=20, weight="bold"),  # タイトル
                region_dropdown,  # 地方選択ドロップダウン
                office_dropdown,  # 詳細地域選択ドロップダウン
                ft.Divider(),     # 区切り線
                ft.Text("天気予報:", size=16),  # 「天気予報:」のラベル
                weather_output,   # 天気予報の表示フィールド
            ],
            expand=True,
        )
    )

# アプリの起動
if __name__ == "__main__":
    ft.app(target=main)
## 改良１