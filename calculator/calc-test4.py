import flet as ft
import math

# ボタンクラス
class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, flex=1):
        super().__init__()
        self.text = text
        self.on_click = button_clicked
        self.data = text
        self.expand = flex

class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, flex=1):
        super().__init__(text, button_clicked, flex)
        self.bgcolor = ft.colors.WHITE24
        self.color = ft.colors.WHITE

class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        super().__init__(text, button_clicked)
        self.bgcolor = ft.colors.ORANGE
        self.color = ft.colors.WHITE

class SciButton(CalcButton):
    def __init__(self, text, button_clicked):
        super().__init__(text, button_clicked)
        self.bgcolor = ft.colors.BLUE
        self.color = ft.colors.WHITE

# 電卓アプリのメインクラス
class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()

        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=30)
        self.bgcolor = ft.colors.BLACK
        self.padding = 10

        self.content = ft.Column(
            expand=True,
            controls=[
                ft.Row([self.result], alignment="end"),
                self.create_button_row(["AC", "(", ")", "/"], is_extra=True),
                self.create_button_row(["7", "8", "9", "*"]),
                self.create_button_row(["4", "5", "6", "-"]),
                self.create_button_row(["1", "2", "3", "+"]),
                self.create_button_row(["0", ".", "="], last_row=True),
                self.create_sci_buttons(),  # 科学電卓用ボタンを追加
            ],
        )

    def create_button_row(self, texts, is_extra=False, last_row=False):
        buttons = []
        for text in texts:
            if is_extra:
                buttons.append(
                    ActionButton(text, self.button_clicked)
                    if text in ["AC", "(", ")"]
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
        return ft.Row(buttons, expand=True)

    def create_sci_buttons(self):
        sci_row1 = ["x^2", "x^y", "e^x", "10^x", "√x"]
        sci_row2 = ["1/x", "x!", "sin", "cos", "tan"]
        sci_row3 = ["ln", "log2", "log10", "π", "Deg"]

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

    def button_clicked(self, e):
        data = e.control.data
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()
        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ".", "(", ")"):
            if self.result.value == "0":
                self.result.value = data
            else:
                self.result.value += data
        elif data in ("+", "-", "*", "/"):
            self.result.value += data
        elif data == "=":
            try:
                self.result.value = str(eval(self.result.value))
            except:
                self.result.value = "Error"
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

        self.update()

    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True

def main(page: ft.Page):
    page.title = "Scientific Calculator"
    page.horizontal_alignment = "stretch"
    page.vertical_alignment = "stretch"
    calc = CalculatorApp()
    page.add(calc)

ft.app(target=main)
