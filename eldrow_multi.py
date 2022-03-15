#!/usr/bin/env python3

from colorama import init, Style, Back
from urllib.request import urlopen
import random
from typing import Literal
import argparse
import pyinputplus as pyip

URLS = {"EN": "https://raw.githubusercontent.com/jason-chao/wordle-solver/main/english_words_original_wordle.txt"}

# TODO still add more type hints
# TODO return scores, maybe save them?
# TODO add docstrings
# TODO turn into module?
# TODO unittesting ;-) ?
# TODO think about what should be inside and/or outside of the class
# ...


def user_settings():
    print("Let's play wordle!")
    n_words = pyip.inputInt(
        "How many words do you want to guess at the same time? (up to 6) ", min=1, max=6)
    n_attempts = pyip.inputInt(
        "How many atttempts would you like to have? (up to 10) ", min=1, max=10)
    cheat = pyip.inputYesNo("Do you want to cheat? [yes/no] ")
    return(n_words, n_attempts, cheat)


class GuessedLetter:
    def __init__(self, letter: str, status: Literal['BLACK', 'YELLOW', 'GREEN']):
        self.status = status
        self.letter = letter


def render_result(evaluated_guess):
    colorama_map = {"GREEN": Back.GREEN,
                    "BLACK": Back.BLACK,
                    "YELLOW": Back.YELLOW}

    for evaluated_letter in evaluated_guess:
        print(colorama_map[evaluated_letter.status], end="")
        print(evaluated_letter.letter, end="")
    print(Style.RESET_ALL)


def get_words(language: str = 'EN') -> list:
    url = URLS.get(language, None)
    if not url:
        raise NotImplementedError(f"Language {language} not available")
    return [line.strip().decode("utf=8") for line in urlopen(url)]


class Wordle():
    def __init__(self, n_words, n_attempts, cheat, language="EN"):
        self.words = get_words(language)
        self.current_attempt = 0
        self.max_attempts = n_attempts
        self.n_words = n_words
        self.cheat = cheat
        self.history = {k: [] for k in range(n_words)}
        self.solution = random.sample(self.words, n_words)
        self.words_solved = [False]*self.n_words
        # we need to initalize colorama as well
        init()

    def _check_guess_valid(self, guess):
        if len(guess) != 5:
            print("Please enter a 5-letter word")
            return False
        elif guess not in self.words:
            print("Unknown word, try again")
            return False
        else:
            return True

    def _check_guess_correct(self, n_word):
        guess = self.history[n_word][-1]
        result = []
        for i in range(len(guess)):
            if guess[i] == self.solution[n_word][i]:
                result.append(GuessedLetter(guess[i], 'GREEN'))
            elif guess[i] in self.solution[n_word][i]:
                result.append(GuessedLetter(guess[i], 'YELLOW'))
            else:
                result.append(GuessedLetter(guess[i], 'BLACK'))
        return result

    def guess(self):
        self.current_attempt += 1
        for i in range(self.n_words):
            if self.words_solved[i] == True:
                continue
            while True:
                current_guess = input(
                    f"[Word {i}, attempt {self.current_attempt}] ")
                if self._check_guess_valid(current_guess):
                    break
            self.history[i].append(current_guess)
            evaluation = self._check_guess_correct(i)
            render_result(evaluation)
            if sum([e.status == "GREEN" for e in evaluation]) == len(evaluation):
                self.words_solved[i] = True
        if all(x == True for x in self.words_solved):
            return True
        else:
            return False

    def play(self):
        if self.cheat:
            print(self.solution)
        while True:
            if self.current_attempt == self.max_attempts:
                print(f"You already had {self.max_attempts} guesses!")
                print("So I guess you lost...")
                print("Maybe make it a bit easier next time")
                break
            guessed = self.guess()
            if guessed:
                print("CONGRATULATIONS!!")
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A Wordle implementation to test out some coding practices")
    args = parser.parse_args()

    settings = user_settings()
    wordle = Wordle(*settings)
    wordle.play()
