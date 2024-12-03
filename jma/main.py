# import flet as ft


# def main(page: ft.Page):
#     page.add(ft.SafeArea(ft.Text("Hello, Flet!")))


# ft.app(main)



import json
from flet import Page, ListView, Text, flet

# JSONファイルを読み込む関数
def load_regions():
    with open("regions.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data["regions"]

# アプリのメイン関数
def main(page: Page):
    page.title = "地域リストビューア"
    page.scroll = "auto"  # スクロール可能にする

    # JSONから地域リストを取得
    regions = load_regions()

    # ListViewを作成してページに追加
    list_view = ListView(spacing=10, padding=20)
    for region in regions:
        list_view.controls.append(Text(region))
    
    page.add(list_view)

# アプリを起動
flet.app(main)
