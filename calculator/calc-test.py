import flet as ft
import math  # 数学関連の関数を使用するためにインポート

# 基本的なボタンのクラス（すべてのボタンの基底クラス）
class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text  # ボタンのラベル
        self.expand = expand  # ボタンのサイズの拡張設定
        self.on_click = button_clicked  # クリック時のイベントハンドラ
        self.data = text  # ボタンのデータ属性

# 数字入力用のボタンクラス
class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        CalcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.colors.WHITE24  # 背景色を設定
        self.color = ft.colors.WHITE  # テキスト色を設定

# 四則演算用のボタンクラス
class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.ORANGE  # 背景色を設定
        self.color = ft.colors.WHITE  # テキスト色を設定

# ACや+/-、%など追加アクション用のボタンクラス
class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.BLUE_GREY_100  # 背景色を設定
        self.color = ft.colors.BLACK  # テキスト色を設定

# 科学計算用ボタンクラス
class SciButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.BLUE  # 背景色を設定
        self.color = ft.colors.WHITE  # テキスト色を設定

# 電卓アプリケーションクラス
class CalculatorApp(ft.Container):
    # アプリケーションの初期化
    def __init__(self):
        super().__init__()
        self.reset()  # 計算状態の初期化

        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=20)  # 計算結果を表示するテキスト
        self.width = 350  # コンテナの幅
        self.bgcolor = ft.colors.BLACK  # 背景色
        self.border_radius = ft.border_radius.all(20)  # コーナーを丸める
        self.padding = 20  # パディングを設定
        self.content = ft.Column(  # コンテンツのレイアウトを縦方向に配置
            controls=[
                ft.Row(controls=[self.result], alignment="end"),  # 結果表示部分
                # 科学計算用のボタン群
                ft.Row(
                    controls=[
                        SciButton(text="sin", button_clicked=self.button_clicked),
                        SciButton(text="cos", button_clicked=self.button_clicked),
                        SciButton(text="tan", button_clicked=self.button_clicked),
                        SciButton(text="log", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        SciButton(text="√x", button_clicked=self.button_clicked),
                        SciButton(text="x²", button_clicked=self.button_clicked),
                        SciButton(text="e^x", button_clicked=self.button_clicked),
                        SciButton(text="1/x", button_clicked=self.button_clicked),
                    ]
                ),
                # 通常の操作ボタン群
                ft.Row(
                    controls=[
                        ExtraActionButton(
                            text="AC", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(
                            text="+/-", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(text="%", button_clicked=self.button_clicked),
                        ActionButton(text="/", button_clicked=self.button_clicked),
                    ]
                ),
                # 以下、省略（他のボタン群）
            ]
        )

    # ボタンがクリックされた際の処理
    def button_clicked(self, e):
        data = e.control.data  # ボタンのデータを取得
        print(f"Button clicked with data = {data}")  # デバッグ用に出力
        if self.result.value == "Error" or data == "AC":
            # "AC"が押された場合やエラー状態の場合、リセット
            self.result.value = "0"
            self.reset()

        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            # 数字や小数点が押された場合の処理
            if self.result.value == "0" or self.new_operand == True:
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value = self.result.value + data

        elif data in ("+", "-", "*", "/"):
            # 四則演算の処理
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.operator = data
            if self.result.value == "Error":
                self.operand1 = "0"
            else:
                self.operand1 = float(self.result.value)
            self.new_operand = True

        elif data in ("="):
            # "="が押された場合の処理
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.reset()

        elif data in ("%"):
            # "%"が押された場合（パーセント計算）
            self.result.value = float(self.result.value) / 100
            self.reset()

        elif data in ("+/-"):
            # 符号反転の処理
            if float(self.result.value) > 0:
                self.result.value = "-" + str(self.result.value)
            elif float(self.result.value) < 0:
                self.result.value = str(
                    self.format_number(abs(float(self.result.value)))
                )

        # 科学計算機の処理
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

        self.update()  # UIの更新

    def format_number(self, num):
        # 整数部分がある場合は整数として表示し、それ以外はそのまま表示
        if num % 1 == 0:
            return int(num)
        else:
            return num

    def reset(self):
        # 計算状態の初期化
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True

# メイン関数。Fletアプリを起動
def main(page: ft.Page):
    page.title = "Calc App"  # ページタイトル
    calc = CalculatorApp()  # 計算機アプリインスタンスを作成
    page.add(calc)  # ページに追加

# アプリケーションを実行
ft.app(target=main)
