import flet as ft  # Fletモジュールをインポート
import math  # 数学関数を使用するためのモジュール

# ボタンクラスの基底クラス。ボタンに表示されるテキストやクリック時の動作を設定する
class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, flex=1):
        super().__init__()
        self.text = text  # ボタンのテキスト
        self.on_click = button_clicked  # ボタンがクリックされたときに実行する関数
        self.data = text  # ボタンのデータ（計算で使用）
        self.expand = flex  # ボタンの横幅を柔軟に調整する

# 数字ボタン専用クラス。CalcButtonを継承
class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, flex=1):
        super().__init__(text, button_clicked, flex)
        self.bgcolor = ft.colors.WHITE24  # ボタン背景色
        self.color = ft.colors.WHITE  # ボタン文字色

# 演算子ボタン専用クラス（+, -, *, /など）。CalcButtonを継承
class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        super().__init__(text, button_clicked)
        self.bgcolor = ft.colors.ORANGE  # ボタン背景色
        self.color = ft.colors.WHITE  # ボタン文字色

# 特殊な機能を持つボタン専用クラス（AC, %, +/-など）。CalcButtonを継承
class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        super().__init__(text, button_clicked)
        self.bgcolor = ft.colors.BLUE_GREY_100  # ボタン背景色
        self.color = ft.colors.BLACK  # ボタン文字色

# 科学計算用ボタンクラス
class SciButton(CalcButton):
    def __init__(self, text, button_clicked):
        super().__init__(text, button_clicked)
        self.bgcolor = ft.colors.BLUE  # 背景色
        self.color = ft.colors.WHITE  # テキスト色

# 計算機全体のクラス。UI構成と計算ロジックを含む
class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()  # 初期化

        # 計算結果を表示するテキスト要素
        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=30)
        self.bgcolor = ft.colors.BLACK  # 背景色
        self.padding = 10  # コンテナの内側余白

        # 計算機のボタンやUI要素を配置
        self.content = ft.Column(
            expand=True,  # コンテナ全体を拡大
            controls=[
                ft.Row([self.result], alignment="end"),  # 結果表示用の行
                self.create_button_row(["AC", "+/-", "%", "/"], is_extra=True),
                self.create_button_row(["7", "8", "9", "*"]),
                self.create_button_row(["4", "5", "6", "-"]),
                self.create_button_row(["1", "2", "3", "+"]),
                self.create_button_row(["0", ".", "="], last_row=True),
                self.create_sci_buttons(),
            ],
        )

    # ボタン行を動的に生成する関数
    def create_button_row(self, texts, is_extra=False, last_row=False):
        buttons = []
        for text in texts:
            if is_extra:
                buttons.append(
                    ExtraActionButton(text, self.button_clicked)
                    if text in ["AC", "+/-", "%"]
                    else ActionButton(text, self.button_clicked)
                )
            elif last_row and text == "0":
                buttons.append(DigitButton(text, self.button_clicked, flex=2))
            else:
                buttons.append(
                    DigitButton(text, self.button_clicked)
                    if text.isdigit() or text == "."
                    else ActionButton(text, self.button_clicked)
                )
        return ft.Row(buttons, expand=True)  # ボタンを横幅いっぱいに配置

    # 科学計算用ボタン行を生成
    def create_sci_buttons(self):
        sci_row1 = ["sin", "cos", "tan", "log"]
        sci_row2 = ["√x", "x²", "e^x", "1/x"]

        return ft.Column(
            controls=[
                ft.Row(
                    [SciButton(text, self.button_clicked) for text in sci_row1],
                    expand=True,
                ),
                ft.Row(
                    [SciButton(text, self.button_clicked) for text in sci_row2],
                    expand=True,
                ),
            ]
        )

    # ボタンがクリックされた際の動作を定義
    def button_clicked(self, e):
        data = e.control.data  # クリックされたボタンのデータを取得
        print(f"Button clicked with data = {data}")  # デバッグ用出力
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"  # エラー状態またはACボタンでリセット
            self.reset()
        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            if self.result.value == "0" or self.new_operand:
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value += data
        elif data in ("+", "-", "*", "/"):
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.operator = data
            if self.result.value == "Error":
                self.operand1 = "0"
            else:
                self.operand1 = float(self.result.value)
            self.new_operand = True
        elif data == "=":
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.reset()
        elif data == "%":
            self.result.value = float(self.result.value) / 100
            self.reset()
        elif data == "+/-":
            if float(self.result.value) > 0:
                self.result.value = "-" + str(self.result.value)
            elif float(self.result.value) < 0:
                self.result.value = str(self.format_number(abs(float(self.result.value))))
        elif data == "sin":
            self.result.value = self.format_number(
                math.sin(math.radians(float(self.result.value)))
            )
        elif data == "cos":
            self.result.value = self.format_number(
                math.cos(math.radians(float(self.result.value)))
            )
        elif data == "tan":
            self.result.value = self.format_number(
                math.tan(math.radians(float(self.result.value)))
            )
        elif data == "log":
            self.result.value = self.format_number(math.log10(float(self.result.value)))
        elif data == "√x":
            self.result.value = self.format_number(math.sqrt(float(self.result.value)))
        elif data == "x²":
            self.result.value = self.format_number(float(self.result.value) ** 2)
        elif data == "e^x":
            self.result.value = self.format_number(math.exp(float(self.result.value)))
        elif data == "1/x":
            if float(self.result.value) != 0:
                self.result.value = self.format_number(1 / float(self.result.value))
            else:
                self.result.value = "Error"
        self.update()  # UIを更新

    def format_number(self, num):
        return int(num) if num % 1 == 0 else num

    def calculate(self, operand1, operand2, operator):
        if operator == "+":
            return self.format_number(operand1 + operand2)
        elif operator == "-":
            return self.format_number(operand1 - operand2)
        elif operator == "*":
            return self.format_number(operand1 * operand2)
        elif operator == "/":
            return "Error" if operand2 == 0 else self.format_number(operand1 / operand2)

    def reset(self):
        self.operator = "+"  # 初期演算子
        self.operand1 = 0  # 初期オペランド
        self.new_operand = True  # 新しいオペランドを入力中かどうかのフラグ

# メイン関数。Fletアプリを起動
def main(page: ft.Page):
    page.title = "Calc App"  # ページタイトル
    page.horizontal_alignment = "stretch"  # 横方向にストレッチ
    page.vertical_alignment = "stretch"  # 縦方向にストレッチ
    calc = CalculatorApp()  # 計算機アプリをインスタンス化
    page.add(calc)  # ページにアプリを追加

ft.app(target=main)  # Fletアプリを起動
