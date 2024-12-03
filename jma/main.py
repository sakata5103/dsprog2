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