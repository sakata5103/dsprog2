import flet as ft  # Fletモジュールをインポート
import math  # 数学関数を使用するためのモジュール

# ボタンクラス
# 電卓の各ボタンに共通する基本的な属性や動作を定義したクラス
class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, flex=1):
        super().__init__()
        self.text = text  # ボタンに表示されるテキスト
        self.on_click = button_clicked  # ボタンがクリックされたときに呼ばれる関数
        self.data = text  # ボタンのデータ（処理に使用）
        self.expand = flex  # ボタンの拡張サイズ（デフォルトは1）

# 数字ボタンのクラス
# 数字入力用のボタンに特化したデザイン
class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, flex=1):
        super().__init__(text, button_clicked, flex)
        self.bgcolor = ft.colors.WHITE24  # ボタンの背景色
        self.color = ft.colors.WHITE  # ボタンの文字色

# 操作ボタンのクラス
# 計算操作用（+、-、*、/ など）のボタンに特化したデザイン
class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        super().__init__(text, button_clicked)
        self.bgcolor = ft.colors.ORANGE  # ボタンの背景色
        self.color = ft.colors.WHITE  # ボタンの文字色

# 科学計算用ボタンのクラス
# 科学電卓の特殊なボタンに特化したデザイン
class SciButton(CalcButton):
    def __init__(self, text, button_clicked):
        super().__init__(text, button_clicked)
        self.bgcolor = ft.colors.BLUE  # ボタンの背景色
        self.color = ft.colors.WHITE  # ボタンの文字色

# 電卓アプリのメインクラス
# 電卓全体のレイアウトと動作を定義
class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()  # 状態のリセット（初期化）

        # 結果表示エリア
        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=30)
        self.bgcolor = ft.colors.BLACK  # 背景色
        self.padding = 10  # パディング設定

        # アプリの全体レイアウト
        self.content = ft.Column(
            expand=True,
            controls=[
                ft.Row([self.result], alignment="end"),  # 計算結果を右揃えで表示
                self.create_button_row(["AC", "(", ")", "/"], is_extra=True),  # 特殊操作ボタン
                self.create_button_row(["7", "8", "9", "*"]),  # 数字と操作ボタン
                self.create_button_row(["4", "5", "6", "-"]),
                self.create_button_row(["1", "2", "3", "+"]),
                self.create_button_row(["0", ".", "="], last_row=True),  # 最下行のボタン
                self.create_sci_buttons(),  # 科学電卓用ボタンを追加
            ],
        )

    # ボタン行を作成する関数
    def create_button_row(self, texts, is_extra=False, last_row=False):
        buttons = []
        for text in texts:
            if is_extra:
                # 特殊ボタン（AC、括弧）の場合
                buttons.append(
                    ActionButton(text, self.button_clicked)
                )
            elif last_row and text == "0":
                # 最下行で0のボタンが拡張されたサイズになる場合
                buttons.append(DigitButton(text, self.button_clicked, flex=2))
            else:
                # 通常の数字または操作ボタンの場合
                buttons.append(
                    DigitButton(text, self.button_clicked)
                    if text.isdigit() or text == "."
                    else ActionButton(text, self.button_clicked)
                )
        return ft.Row(buttons, expand=True)  # ボタンを1行に配置

    # 科学電卓用のボタンを作成する関数
    def create_sci_buttons(self):
        sci_row1 = ["x^2", "x^y", "e^x", "10^x", "√x"]  # 最初の行
        sci_row2 = ["1/x", "x!", "sin", "cos", "tan"]  # 2行目
        sci_row3 = ["ln", "log2", "log10", "π", "Deg"]  # 3行目

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
                ft.Row(
                    [SciButton(text, self.button_clicked) for text in sci_row3],
                    expand=True,
                ),
            ]
        )

    # ボタンがクリックされたときの動作を定義
    def button_clicked(self, e):
        data = e.control.data  # クリックされたボタンのデータを取得
        if self.result.value == "Error" or data == "AC":
            # エラー状態やACボタンが押されたときにリセット
            self.result.value = "0"
            self.reset()
        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ".", "(", ")"):
            # 数字や括弧が入力されたとき
            if self.result.value == "0":
                self.result.value = data
            else:
                self.result.value += data
        elif data in ("+", "-", "*", "/"):
            # 四則演算の演算子が入力されたとき
            self.result.value += data
        elif data == "=":
            # 計算を実行
            try:
                self.result.value = str(eval(self.result.value))  # evalを使用して計算
            except:
                self.result.value = "Error"  # エラー時に表示
        # 以下、科学電卓の操作ごとに処理を定義
        elif data == "x^2":
            self.result.value = str(float(self.result.value) ** 2)
        elif data == "x^y":
            self.result.value += "**"
        elif data == "e^x":
            self.result.value = str(math.exp(float(self.result.value)))
        elif data == "10^x":
            self.result.value = str(10 ** float(self.result.value))
        elif data == "√x":
            self.result.value = str(math.sqrt(float(self.result.value)))
        elif data == "1/x":
            self.result.value = str(1 / float(self.result.value))
        elif data == "x!":
            self.result.value = str(math.factorial(int(self.result.value)))
        elif data == "sin":
            self.result.value = str(math.sin(math.radians(float(self.result.value))))
        elif data == "cos":
            self.result.value = str(math.cos(math.radians(float(self.result.value))))
        elif data == "tan":
            self.result.value = str(math.tan(math.radians(float(self.result.value))))
        elif data == "ln":
            self.result.value = str(math.log(float(self.result.value)))
        elif data == "log2":
            self.result.value = str(math.log2(float(self.result.value)))
        elif data == "log10":
            self.result.value = str(math.log10(float(self.result.value)))
        elif data == "π":
            self.result.value = str(math.pi)
        elif data == "Deg":
            self.result.value = str(math.degrees(float(self.result.value)))

        self.update()  # 画面を更新

    # 状態をリセットする関数
    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True

# アプリのエントリーポイント
def main(page: ft.Page):
    page.title = "Scientific Calculator"  # アプリのタイトル
    page.horizontal_alignment = "stretch"  # 横方向にストレッチ
    page.vertical_alignment = "stretch"  # 縦方向にストレッチ
    calc = CalculatorApp()  # 電卓アプリのインスタンスを作成
    page.add(calc)  # ページに追加

ft.app(target=main)  # アプリを起動
