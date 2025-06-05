import random

class GuessNumberGame:
    def __init__(self):
        self.min_num = 0
        self.max_num = 100
        self.secret_number = None
        self.max_attempts = 5
        self.attempts_left = self.max_attempts
        self.game_active = False

    def start_game(self, min_num, max_num):
        self.min_num = min_num
        self.max_num = max_num
        self.secret_number = random.randint(min_num, max_num)
        self.attempts_left = self.max_attempts
        self.game_active = True

    def check_guess(self, guess):
        if not self.game_active:
            return "Гра не розпочата"
        if self.attempts_left <= 0:
            self.game_active = False
            return "Спроб більше немає"

        self.attempts_left -= 1

        if guess == self.secret_number:
            self.game_active = False
            return "correct"

        if self.attempts_left == 0:
            self.game_active = False

        return "higher" if guess < self.secret_number else "lower"

    def is_game_active(self):
        return self.game_active
