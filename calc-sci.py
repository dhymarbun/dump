import tkinter as tk
from tkinter import messagebox
from math import *

BG_COLOR = "#1f1f1f"
BUTTON_COLOR = "#4caf50"
BUTTON_TEXT_COLOR = "#ffffff"
DISPLAY_COLOR = "#000000"
FONT = ("Helvetica", 18, "bold")
BUTTON_FONT = ("Helvetica", 14)

class FuturisticCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("greeny weird lookin ahh calc")
        self.root.geometry("400x600")
        self.root.configure(bg=BG_COLOR)

        self.expression = ""

        self.display = tk.Entry(
            root,
            font=FONT,
            bg=DISPLAY_COLOR,
            fg=BUTTON_TEXT_COLOR,
            justify="right",
            bd=10,
            insertwidth=2
        )
        self.display.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=20, sticky="nsew")

        self.create_buttons()

    def add_to_expression(self, value):
        self.expression += str(value)
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.expression)

    def calculate(self):
        try:
            result = eval(self.expression)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, result)
            self.expression = str(result)
        except Exception as e:
            messagebox.showerror("Error", "Invalid Expression")
            self.clear()

    def clear(self):
        self.expression = ""
        self.display.delete(0, tk.END)

    def create_buttons(self):
        buttons = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
            ("C", 5, 0), ("sin", 5, 1), ("cos", 5, 2), ("tan", 5, 3),
            ("log", 6, 0), ("ln", 6, 1), ("sqrt", 6, 2), ("^", 6, 3),
        ]

        for text, row, col in buttons:
            self.create_button(text, row, col)

    def create_button(self, text, row, col):
        command = lambda: self.add_to_expression(text) if text not in ["=", "C", "sqrt", "^", "sin", "cos", "tan", "log", "ln"] else None
        if text == "=":
            command = self.calculate
        elif text == "C":
            command = self.clear
        elif text == "sqrt":
            command = lambda: self.add_to_expression("sqrt(")
        elif text == "^":
            command = lambda: self.add_to_expression("**")
        elif text in ["sin", "cos", "tan", "log", "ln"]:
            command = lambda t=text: self.add_to_expression(f"{t}(")

        btn = tk.Button(
            self.root,
            text=text,
            font=BUTTON_FONT,
            bg=BUTTON_COLOR,
            fg=BUTTON_TEXT_COLOR,
            command=command,
            relief="flat",
            activebackground="#3e8e41",
            activeforeground=BUTTON_TEXT_COLOR
        )
        btn.grid(row=row, column=col, ipadx=20, ipady=10, sticky="nsew")


if __name__ == "__main__":
    root = tk.Tk()
    app = FuturisticCalculator(root)

    for i in range(7):
        root.grid_rowconfigure(i, weight=1)
    for i in range(4):
        root.grid_columnconfigure(i, weight=1)

    root.mainloop()
