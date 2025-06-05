import tkinter as tk
from tkinter import messagebox
from core.game_logic import GuessNumberGame

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Вгадай число")
        self.game = GuessNumberGame()
        self.build_ui()

    def build_ui(self):
        frame = tk.Frame(self.root, padx=15, pady=15)
        frame.pack()

        tk.Label(frame, text="Мінімальне число:").grid(row=0, column=0, sticky="e")
        self.min_entry = tk.Entry(frame, width=10)
        self.min_entry.grid(row=0, column=1)

        tk.Label(frame, text="Максимальне число:").grid(row=1, column=0, sticky="e")
        self.max_entry = tk.Entry(frame, width=10)
        self.max_entry.grid(row=1, column=1)

        self.start_button = tk.Button(frame, text="Почати гру", command=self.start_game)
        self.start_button.grid(row=2, column=0, columnspan=2, pady=10)

        tk.Label(frame, text="Ваша спроба:").grid(row=3, column=0, sticky="e")
        self.guess_entry = tk.Entry(frame, width=10, state="disabled")
        self.guess_entry.grid(row=3, column=1)

        self.check_button = tk.Button(frame, text="Перевірити", state="disabled", command=self.check_guess)
        self.check_button.grid(row=4, column=0, columnspan=2, pady=5)

        self.feedback_label = tk.Label(frame, text="", fg="blue")
        self.feedback_label.grid(row=5, column=0, columnspan=2)

    def start_game(self):
        try:
            min_num = int(self.min_entry.get())
            max_num = int(self.max_entry.get())
        except ValueError:
            messagebox.showerror("Помилка", "Введіть коректні цілі числа.")
            return

        if min_num >= max_num:
            messagebox.showerror("Помилка", "Мінімальне число має бути менше за максимальне.")
            return

        self.game.start_game(min_num, max_num)
        self.feedback_label.config(text=f"Гра почалась! У вас {self.game.max_attempts} спроб.", fg="blue")
        self.guess_entry.config(state="normal")
        self.check_button.config(state="normal")
        self.min_entry.config(state="disabled")
        self.max_entry.config(state="disabled")
        self.start_button.config(state="disabled")
        self.guess_entry.delete(0, tk.END)

    def check_guess(self):
        if not self.game.is_game_active():
            # Гра завершена — показуємо загадане число
            self.feedback_label.config(
                text=f"Гра завершена! Загадане число було {self.game.secret_number}.", fg="red"
            )
            return

        try:
            guess = int(self.guess_entry.get())
        except ValueError:
            messagebox.showerror("Помилка", "Введіть ціле число.")
            return

        result = self.game.check_guess(guess)

        messages = {
            "correct": (f"🎉 Вірно! Загадане число було {self.game.secret_number}.", "green", True),
            "higher": (f"Спробуйте більше число! Залишилось спроб: {self.game.attempts_left}", "orange", False),
            "lower": (f"Спробуйте менше число! Залишилось спроб: {self.game.attempts_left}", "orange", False),
            "Спроб більше немає": (f"Гру завершено! Загадане число було {self.game.secret_number}.", "red", True)
        }

        msg, color, end_game_flag = messages.get(result, ("Невідома помилка", "black", False))
        self.feedback_label.config(text=msg, fg=color)

        if end_game_flag:
            self.end_game()

        self.guess_entry.delete(0, tk.END)

    def end_game(self):
        self.guess_entry.config(state="disabled")
        self.check_button.config(state="disabled")
        self.start_button.config(state="normal")
        self.min_entry.config(state="normal")
        self.max_entry.config(state="normal")
