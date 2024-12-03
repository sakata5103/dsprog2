##1
# import flet as ft
# import requests

# API_URL = "http://www.jma.go.jp/bosai/common/const/area.json"

# def main(page: ft.Page):
#     # ページ設定
#     page.title = "地域リストアプリ"
#     page.scroll = "auto"

#     # 初期データ取得
#     try:
#         response = requests.get(API_URL)
#         response.raise_for_status()
#         data = response.json()
#         regions = {code: info["name"] for code, info in data["centers"].items()}
#     except Exception as e:
#         page.add(ft.Text(f"データの取得に失敗しました: {e}", color=ft.colors.RED))
#         return

#     # ウィジェットの定義
#     region_dropdown = ft.Dropdown(
#         label="地方を選択",
#         options=[ft.dropdown.Option(key, value) for key, value in regions.items()],
#         on_change=lambda e: update_offices(e.control.value),
#     )
#     office_list = ft.ListView(expand=True)

#     # 地方選択後の更新処理
#     def update_offices(region_code):
#         office_list.controls.clear()  # 一度リストをリセット
#         if not region_code:
#             page.update()
#             return

#         # 選択された地方の詳細情報を取得
#         try:
#             offices = []
#             region_data = data["centers"].get(region_code)
#             if region_data:
#                 for child_code in region_data["children"]:
#                     offices.append(f"{region_data['officeName']} (コード: {child_code})")
#         except Exception as e:
#             offices = [f"エラー: {e}"]

#         # リストビューを更新
#         office_list.controls.extend([ft.Text(office) for office in offices])
#         page.update()

#     # ページにウィジェットを追加
#     page.add(
#         ft.Column(
#             [
#                 ft.Text("地域リストアプリ", size=20, weight="bold"),
#                 region_dropdown,
#                 ft.Divider(),
#                 ft.Text("詳細地域リスト:"),
#                 office_list,
#             ],
#             expand=True,
#         )
#     )

# # アプリの起動
# if __name__ == "__main__":
#     ft.app(target=main)
##1



##2
# import flet as ft
# import requests

# # APIエンドポイント
# AREA_API_URL = "http://www.jma.go.jp/bosai/common/const/area.json"
# FORECAST_API_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/{}.json"

# def main(page: ft.Page):
#     page.title = "天気予報アプリ"
#     page.scroll = "auto"

#     # 地域データの取得
#     try:
#         area_response = requests.get(AREA_API_URL)
#         area_response.raise_for_status()
#         area_data = area_response.json()
#         regions = {code: info["name"] for code, info in area_data["centers"].items()}
#     except Exception as e:
#         page.add(ft.Text(f"地域データの取得に失敗しました: {e}", color=ft.colors.RED))
#         return

#     # UIウィジェット
#     region_dropdown = ft.Dropdown(
#         label="地方を選択",
#         options=[ft.dropdown.Option(key, value) for key, value in regions.items()],
#         on_change=lambda e: update_offices(e.control.value),
#     )
#     office_dropdown = ft.Dropdown(
#         label="地域を選択",
#         options=[],
#         on_change=lambda e: fetch_weather(e.control.value),
#     )
#     weather_output = ft.ListView(expand=True)

#     # 地方選択時の処理
#     def update_offices(region_code):
#         office_dropdown.options.clear()
#         weather_output.controls.clear()
#         if not region_code:
#             page.update()
#             return

#         region_info = area_data["centers"].get(region_code)
#         if region_info:
#             for child_code in region_info["children"]:
#                 child_name = next(
#                     (area["name"] for area in area_data["offices"].values() if area["code"] == child_code),
#                     "不明な地域",
#                 )
#                 office_dropdown.options.append(ft.dropdown.Option(child_code, child_name))
#         page.update()

#     # 天気予報の取得と表示
#     def fetch_weather(region_code):
#         weather_output.controls.clear()
#         if not region_code:
#             page.update()
#             return

#         try:
#             forecast_response = requests.get(FORECAST_API_URL.format(region_code))
#             forecast_response.raise_for_status()
#             forecast_data = forecast_response.json()

#             # 天気情報の整形
#             for series in forecast_data[0]["timeSeries"]:
#                 times = series["timeDefines"]
#                 for area in series["areas"]:
#                     if area["area"]["code"] == region_code:
#                         weather_output.controls.append(
#                             ft.Text(f"地域: {area['area']['name']}", weight="bold", size=16)
#                         )
#                         for i, time in enumerate(times):
#                             weather_output.controls.append(
#                                 ft.Text(
#                                     f"日時: {time} - 天気: {area.get('weathers', ['不明'])[i]} - "
#                                     f"風: {area.get('winds', ['不明'])[i]} - 波: {area.get('waves', ['不明'])[i]}"
#                                 )
#                             )
#                         break

#         except Exception as e:
#             weather_output.controls.append(ft.Text(f"天気情報の取得に失敗しました: {e}", color=ft.colors.RED))
#         page.update()

#     # ページにUIを追加
#     page.add(
#         ft.Column(
#             [
#                 ft.Text("天気予報アプリ", size=20, weight="bold"),
#                 region_dropdown,
#                 office_dropdown,
#                 ft.Divider(),
#                 ft.Text("天気情報:"),
#                 weather_output,
#             ],
#             expand=True,
#         )
#     )

# # アプリ起動
# if __name__ == "__main__":
#     ft.app(target=main)
##2



##3　天気情報が一つしか表示されない
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
#     except Exception as e:
#         page.add(ft.Text(f"データの取得に失敗しました: {e}", color=ft.colors.RED))
#         return

#     # ウィジェットの定義
#     region_dropdown = ft.Dropdown(
#         label="地方を選択",
#         options=[ft.dropdown.Option(key, value) for key, value in regions.items()],
#         on_change=lambda e: update_offices(e.control.value),
#     )
#     office_dropdown = ft.Dropdown(label="詳細地域を選択", disabled=True)
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
#                     ft.dropdown.Option(child, f"{region_data['officeName']} ({child})")
#                     for child in region_data["children"]
#                 ]
#                 office_dropdown.disabled = False
#         except Exception as e:
#             weather_output.value = f"詳細地域の取得に失敗しました: {e}"

#         page.update()

#     # 天気予報を取得して表示
#     def fetch_weather(e):
#         selected_code = office_dropdown.value
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
#             forecasts = latest_weather["timeSeries"][0]["areas"][0]

#             # 表示用の文字列を作成
#             forecast_text = (
#                 f"発表機関: {publishing_office}\n"
#                 f"発表日時: {report_datetime}\n"
#                 f"地域: {forecasts['area']['name']}\n"
#             )
#             for time, weather in zip(
#                 latest_weather["timeSeries"][0]["timeDefines"],
#                 forecasts["weathers"],
#             ):
#                 forecast_text += f"{time}: {weather}\n"

#             weather_output.value = forecast_text
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
#                 ft.ElevatedButton("天気予報を取得", on_click=fetch_weather),
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
##3



##4　天気情報がうまく表示されない
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
#     except Exception as e:
#         page.add(ft.Text(f"データの取得に失敗しました: {e}", color=ft.colors.RED))
#         return

#     # ウィジェットの定義
#     region_dropdown = ft.Dropdown(
#         label="地方を選択",
#         options=[ft.dropdown.Option(key, value) for key, value in regions.items()],
#         on_change=lambda e: update_offices(e.control.value),
#     )
#     office_dropdown = ft.Dropdown(label="詳細地域を選択", disabled=True)
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
#                     ft.dropdown.Option(child, f"{region_data['officeName']} ({child})")
#                     for child in region_data["children"]
#                 ]
#                 office_dropdown.disabled = False
#         except Exception as e:
#             weather_output.value = f"詳細地域の取得に失敗しました: {e}"

#         page.update()

#     # 天気予報を取得して表示
#     def fetch_weather(e):
#         selected_code = office_dropdown.value
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

#             # 必要な情報を抽出して表示
#             forecast_text = ""
#             for forecast in weather_data:
#                 publishing_office = forecast["publishingOffice"]
#                 report_datetime = forecast["reportDatetime"]
#                 time_series = forecast["timeSeries"][0]

#                 forecast_text += (
#                     f"発表機関: {publishing_office}\n"
#                     f"発表日時: {report_datetime}\n\n"
#                 )

#                 for area in time_series["areas"]:
#                     area_name = area["area"]["name"]
#                     weathers = area["weathers"]
#                     time_defines = time_series["timeDefines"]

#                     forecast_text += f"地域: {area_name}\n"
#                     for time, weather in zip(time_defines, weathers):
#                         forecast_text += f"{time}: {weather}\n"
#                     forecast_text += "\n"

#             weather_output.value = forecast_text
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
#                 ft.ElevatedButton("天気予報を取得", on_click=fetch_weather),
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
##4





##5　無駄な情報が表示される
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
#     except Exception as e:
#         page.add(ft.Text(f"データの取得に失敗しました: {e}", color=ft.colors.RED))
#         return

#     # ウィジェットの定義
#     region_dropdown = ft.Dropdown(
#         label="地方を選択",
#         options=[ft.dropdown.Option(key, value) for key, value in regions.items()],
#         on_change=lambda e: update_offices(e.control.value),
#     )
#     office_dropdown = ft.Dropdown(label="詳細地域を選択", disabled=True)
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
#                     ft.dropdown.Option(child, f"{region_data['officeName']} ({child})")
#                     for child in region_data["children"]
#                 ]
#                 office_dropdown.disabled = False
#         except Exception as e:
#             weather_output.value = f"詳細地域の取得に失敗しました: {e}"

#         page.update()

#     # 天気予報を取得して表示
#     def fetch_weather(e):
#         selected_code = office_dropdown.value
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
#                     forecast_text += f"地域: {area['area']['name']}\n"
#                     for time, weather, wind in zip(
#                         time_defines,
#                         area.get("weathers", []),
#                         area.get("winds", []),
#                     ):
#                         forecast_text += f"{time}: 天気: {weather}, 風: {wind}\n"
#                     forecast_text += "\n"

#             weather_output.value = forecast_text
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
#                 ft.ElevatedButton("天気予報を取得", on_click=fetch_weather),
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
##5




##6　いいけど、改善したい
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
#     except Exception as e:
#         page.add(ft.Text(f"データの取得に失敗しました: {e}", color=ft.colors.RED))
#         return

#     # ウィジェットの定義
#     region_dropdown = ft.Dropdown(
#         label="地方を選択",
#         options=[ft.dropdown.Option(key, value) for key, value in regions.items()],
#         on_change=lambda e: update_offices(e.control.value),
#     )
#     office_dropdown = ft.Dropdown(label="詳細地域を選択", disabled=True)
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
#                     ft.dropdown.Option(child, f"{region_data['officeName']} ({child})")
#                     for child in region_data["children"]
#                 ]
#                 office_dropdown.disabled = False
#         except Exception as e:
#             weather_output.value = f"詳細地域の取得に失敗しました: {e}"

#         page.update()

#     # 天気予報を取得して表示
#     def fetch_weather(e):
#         selected_code = office_dropdown.value
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
#                             forecast_text += f"{time}: 天気: {weather}, 風: {wind}\n"
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
#                 ft.ElevatedButton("天気予報を取得", on_click=fetch_weather),
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
##6




##7　完成でもいい
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
#     office_dropdown = ft.Dropdown(label="詳細地域を選択", disabled=True)
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
#     def fetch_weather(e):
#         selected_code = office_dropdown.value
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
#                             forecast_text += f"{time}: 天気: {weather}, 風: {wind}\n"
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
#                 ft.ElevatedButton("天気予報を取得", on_click=fetch_weather),
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
##7






##8　これで完成でもいい２
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
#                             forecast_text += f"{time}: 天気: {weather}, 風: {wind}\n"
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
##8




##9
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
#                             forecast_text += f"{time}\n    天気: {weather}\n    風: {wind}\n\n"
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
##9



###10 完成でもいい3
import flet as ft
import requests

BASE_API_URL = "http://www.jma.go.jp/bosai/common/const/area.json"
WEATHER_API_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/"

def main(page: ft.Page):
    # ページ設定
    page.title = "地域別天気予報アプリ"
    page.scroll = "auto"

    # 初期データ取得
    try:
        response = requests.get(BASE_API_URL)
        response.raise_for_status()
        data = response.json()
        regions = {code: info["name"] for code, info in data["centers"].items()}
        offices = data["offices"]
    except Exception as e:
        page.add(ft.Text(f"データの取得に失敗しました: {e}", color=ft.colors.RED))
        return

    # ウィジェットの定義
    region_dropdown = ft.Dropdown(
        label="地方を選択",
        options=[ft.dropdown.Option(key, value) for key, value in regions.items()],
        on_change=lambda e: update_offices(e.control.value),
    )
    office_dropdown = ft.Dropdown(label="詳細地域を選択", disabled=True, on_change=lambda e: fetch_weather(e.control.value))
    weather_output = ft.Text(expand=True)

    # 地方選択後の更新処理
    def update_offices(region_code):
        office_dropdown.options.clear()
        office_dropdown.disabled = True
        weather_output.value = ""
        page.update()

        if not region_code:
            return

        # 地方コードに基づく詳細地域を取得
        try:
            region_data = data["centers"].get(region_code)
            if region_data:
                office_dropdown.options = [
                    ft.dropdown.Option(
                        child,
                        f"{offices[child]['name']} ({offices[child]['officeName']})"
                    )
                    for child in region_data["children"] if child in offices
                ]
                office_dropdown.disabled = False
        except Exception as e:
            weather_output.value = f"詳細地域の取得に失敗しました: {e}"

        page.update()

    # 天気予報を取得して表示
    def fetch_weather(selected_code):
        weather_output.value = ""
        if not selected_code:
            weather_output.value = "詳細地域を選択してください。"
            page.update()
            return

        # 天気情報を取得
        try:
            response = requests.get(f"{WEATHER_API_URL}{selected_code}.json")
            response.raise_for_status()
            weather_data = response.json()

            # 必要な情報を抽出
            latest_weather = weather_data[0]  # 最初の要素が最新のデータ
            publishing_office = latest_weather["publishingOffice"]
            report_datetime = latest_weather["reportDatetime"]
            time_series = latest_weather["timeSeries"]

            # 表示用の文字列を作成
            forecast_text = f"発表機関: {publishing_office}\n発表日時: {report_datetime}\n\n"

            for series in time_series:
                time_defines = series["timeDefines"]
                for area in series["areas"]:
                    # 天気情報が存在するエリアのみ取得
                    if "weathers" in area:
                        forecast_text += f"地域: {area['area']['name']}\n"
                        for time, weather, wind in zip(
                            time_defines,
                            area.get("weathers", []),
                            area.get("winds", []),
                        ):
                            forecast_text += f"\n    日付: {time}\n    天気: {weather}\n    風: {wind}\n"

                        forecast_text += "\n"

            weather_output.value = forecast_text if forecast_text.strip() else "天気情報がありません。"
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
##10