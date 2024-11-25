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
class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()  # 初期化

        # 計算結果を表示するテキスト要素
        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=20)
        self.width = 350  # 計算機の横幅
        self.bgcolor = ft.colors.BLACK  # 背景色
        self.border_radius = ft.border_radius.all(20)  # 角の丸み
        self.padding = 20  # コンテナの内側余白

        

        # 計算機のボタンやUI要素を配置
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment="end"),  # 結果表示用の行
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
                ft.Row(
                    controls=[
                        DigitButton(text="7", button_clicked=self.button_clicked),
                        DigitButton(text="8", button_clicked=self.button_clicked),
                        DigitButton(text="9", button_clicked=self.button_clicked),
                        ActionButton(text="*", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="4", button_clicked=self.button_clicked),
                        DigitButton(text="5", button_clicked=self.button_clicked),
                        DigitButton(text="6", button_clicked=self.button_clicked),
                        ActionButton(text="-", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="1", button_clicked=self.button_clicked),
                        DigitButton(text="2", button_clicked=self.button_clicked),
                        DigitButton(text="3", button_clicked=self.button_clicked),
                        ActionButton(text="+", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(
                            text="0", expand=2, button_clicked=self.button_clicked
                        ),
                        DigitButton(text=".", button_clicked=self.button_clicked),
                        ActionButton(text="=", button_clicked=self.button_clicked),
                
                # 科学計算機機能を追加
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

                
                    ]
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
            # 数字や小数点の入力処理
            if self.result.value == "0" or self.new_operand:
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value += data

        elif data in ("+", "-", "*", "/"):
            # 演算子の入力処理
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
            # 計算結果を表示
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.reset()

        elif data == "%":
            # パーセント計算
            self.result.value = float(self.result.value) / 100
            self.reset()

        elif data == "+/-":
            # 符号反転
            if float(self.result.value) > 0:
                self.result.value = "-" + str(self.result.value)
            elif float(self.result.value) < 0:
                self.result.value = str(self.format_number(abs(float(self.result.value))))





        # 科学計算機の機能の処理
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

    # 数字のフォーマット（整数の場合は小数点を表示しない）
    def format_number(self, num):
        if num % 1 == 0:
            return int(num)
        else:
            return num

    # 演算処理を行う関数
    def calculate(self, operand1, operand2, operator):
        if operator == "+":
            return self.format_number(operand1 + operand2)
        elif operator == "-":
            return self.format_number(operand1 - operand2)
        elif operator == "*":
            return self.format_number(operand1 * operand2)
        elif operator == "/":
            if operand2 == 0:
                return "Error"  # 0除算エラー
            else:
                return self.format_number(operand1 / operand2)

    # リセット処理（初期化）
    def reset(self):
        self.operator = "+"  # 初期演算子
        self.operand1 = 0  # 初期オペランド
        self.new_operand = True  # 新しいオペランドを入力中かどうかのフラグ

# メイン関数。Fletアプリを起動
def main(page: ft.Page):
    page.title = "Calc App"  # ページタイトル
    calc = CalculatorApp()  # 計算機アプリインスタンスを作成
    page.add(calc)  # ページに追加

# アプリケーションを実行
ft.app(target=main)
