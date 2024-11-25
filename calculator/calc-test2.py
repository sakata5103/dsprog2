import flet as ft  # Fletモジュールをインポート
import math  # 数学関数を使用するためのモジュール

# ボタンクラスの基底クラス。ボタンに表示されるテキストやクリック時の動作を設定する
class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text  # ボタンのテキスト
        self.expand = expand  # ボタンの横方向の拡大比率
        self.on_click = button_clicked  # ボタンがクリックされたときに実行する関数
        self.data = text  # ボタンのデータ（計算で使用）

# 数字ボタン専用クラス。CalcButtonを継承
class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        CalcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.colors.WHITE24  # ボタン背景色
        self.color = ft.colors.WHITE  # ボタン文字色

# 演算子ボタン専用クラス（+, -, *, /など）。CalcButtonを継承
class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.ORANGE  # ボタン背景色
        self.color = ft.colors.WHITE  # ボタン文字色

# 特殊な機能を持つボタン専用クラス（AC, %, +/-など）。CalcButtonを継承
class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.BLUE_GREY_100  # ボタン背景色
        self.color = ft.colors.BLACK  # ボタン文字色

# 科学計算用ボタンクラス
class SciButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.BLUE  # 背景色を設定
        self.color = ft.colors.WHITE  # テキスト色を設定

# 計算機全体のクラス。UI構成と計算ロジックを含む
class CalculatorApp(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.reset()  # 初期化

    def build(self):
        # 計算結果を表示するテキスト要素
        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=30)
        
        # ボタンを格納する全体レイアウトを定義
        return ft.Container(
            width=400,  # 横幅を設定
            height=600,  # 高さを設定
            bgcolor=ft.colors.BLACK,  # 背景色を設定
            padding=20,  # 全体の余白を設定
            content=ft.Column(
                spacing=10,  # 各行の間隔
                controls=[
                    ft.Container(
                        height=80,
                        content=ft.Row(
                            controls=[self.result], alignment="end"  # 結果表示行
                        ),
                    ),
                    # ボタンの行を順に追加
                    ft.Row(
                        controls=[
                            ExtraActionButton("AC", self.button_clicked),
                            ExtraActionButton("+/-", self.button_clicked),
                            ExtraActionButton("%", self.button_clicked),
                            ActionButton("/", self.button_clicked),
                        ],
                    ),
                    ft.Row(
                        controls=[
                            DigitButton("7", self.button_clicked),
                            DigitButton("8", self.button_clicked),
                            DigitButton("9", self.button_clicked),
                            ActionButton("*", self.button_clicked),
                        ],
                    ),
                    ft.Row(
                        controls=[
                            DigitButton("4", self.button_clicked),
                            DigitButton("5", self.button_clicked),
                            DigitButton("6", self.button_clicked),
                            ActionButton("-", self.button_clicked),
                        ],
                    ),
                    ft.Row(
                        controls=[
                            DigitButton("1", self.button_clicked),
                            DigitButton("2", self.button_clicked),
                            DigitButton("3", self.button_clicked),
                            ActionButton("+", self.button_clicked),
                        ],
                    ),
                    ft.Row(
                        controls=[
                            DigitButton("0", self.button_clicked, expand=2),
                            DigitButton(".", self.button_clicked),
                            ActionButton("=", self.button_clicked),
                        ],
                    ),
                    ft.Row(
                        controls=[
                            SciButton("sin", self.button_clicked),
                            SciButton("cos", self.button_clicked),
                            SciButton("tan", self.button_clicked),
                            SciButton("log", self.button_clicked),
                        ],
                    ),
                    ft.Row(
                        controls=[
                            SciButton("√x", self.button_clicked),
                            SciButton("x²", self.button_clicked),
                            SciButton("e^x", self.button_clicked),
                            SciButton("1/x", self.button_clicked),
                        ],
                    ),
                ],
            ),
        )

    # ボタンがクリックされた際の動作を定義
    def button_clicked(self, e):
        data = e.control.data  # ボタンのデータを取得
        print(f"Button clicked with data = {data}")  # デバッグ用

        if data == "AC":
            self.result.value = "0"  # 初期化
            self.reset()

    # リセット処理
    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True

# メイン関数。Fletアプリを起動
def main(page: ft.Page):
    page.title = "Calculator"
    calc = CalculatorApp()  # 計算機アプリのインスタンス
    page.add(calc)  # ページに追加

ft.app(target=main)
