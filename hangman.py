import random
import enum

MENU_TEXT = 'Type "play" to play the game, "score" to show the scoreboard, and "exit" to quit:'

GUESS_TEXT = 'Guess the word '
WIN_FAIL_TEXT = {True: 'You guessed the word {}!\nYou survived!',
                 False: 'You lost!'
                 }

SCOREBOARD_TEXT = 'You won: {:d} times.\nYou lost: {:d} times.'

END_TEXT = 'Thanks for playing!'
WRONG_LETTER_TEXT = "That letter doesn't appear in the word."
NON_LETTER_TEXT = 'Please, enter a lowercase letter from the English alphabet.'
WRONG_NUM_LETTERS = 'Please, input a single letter.'
NO_IMPROVEMENTS_TEXT = 'No improvements.'
ALREADY_TRIED_TEXT = "You've already guessed this letter"
BYE_TEXT = 'Bye!'
ASK_LETTER_TEXT = 'Input a letter:'

POSSIBLE_GOAL_WORDS = ('python', 'java', 'swift', 'javascript', 'pascal', 'golang', 'rust', 'haskell', 'basic',
                       'fortran', 'ada', 'cobol', 'php', 'erlang', 'forth', 'prolog', 'lisp')

NUM_ATTEMPTS = 8


class GameState(enum.Enum):
    idle = 0
    in_menu = 1
    playing = 2
    quit = 4


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += 1


class Hangman:
    def __init__(self, game_id):
        self.id = game_id
        self.state = GameState.idle
        self.num_of_wins = 0
        self.num_of_fails = 0
        self.reset()
        self.goal_word = random.choice(POSSIBLE_GOAL_WORDS)
        self.num_of_attempts = NUM_ATTEMPTS
        self.guess_word = '-' * len(self.goal_word)
        self.guess_history = ''
        self.win = False

    def reset(self):
        self.goal_word = random.choice(POSSIBLE_GOAL_WORDS)
        self.num_of_attempts = NUM_ATTEMPTS
        self.guess_word = '-' * len(self.goal_word)
        self.guess_history = ''
        self.win = False

    def try_letter(self, letter):
        success = 0
        if not len(letter) == 1:
            result = WRONG_NUM_LETTERS
        elif letter < 'a' or letter > 'z':
            result = NON_LETTER_TEXT
        elif letter in self.guess_history:
            result = ALREADY_TRIED_TEXT
        else:
            self.guess_history += letter
            if letter in self.goal_word:
                self.guess_word = list(self.guess_word)
                indxs = list(find_all(self.goal_word, letter))
                for indx in indxs:
                    self.guess_word[indx] = letter
                self.guess_word = ''.join(self.guess_word)
                success = 1
                result = self.guess_word + '\n' + ASK_LETTER_TEXT
            else:
                result = WRONG_LETTER_TEXT
                success = -1
        return success, result

    def proceed(self, user_input):
        answer = ''
        if self.state == GameState.idle:
            self.state = GameState.in_menu
            answer = MENU_TEXT
        elif self.state == GameState.in_menu:
            if user_input == 'play':
                self.state = GameState.playing
                answer = self.guess_word + '\n' + ASK_LETTER_TEXT
            elif user_input == 'score':
                self.state = GameState.in_menu
                answer = SCOREBOARD_TEXT.format(self.num_of_wins, self.num_of_fails)
            elif user_input == 'exit':
                self.state = GameState.quit
                answer = BYE_TEXT
            else:
                self.state = GameState.in_menu
                answer = MENU_TEXT
        elif self.state == GameState.quit:
            pass
        elif self.state == GameState.playing:
            if self.num_of_attempts > 1:
                result, answer = self.try_letter(user_input)
                if result < 0:
                    self.num_of_attempts -= 1
                else:
                    if self.goal_word == self.guess_word:
                        self.win = True
                        self.state = GameState.in_menu
                        answer = WIN_FAIL_TEXT[self.win].format(self.goal_word)
                        answer += '\n' + MENU_TEXT
                        self.num_of_wins += 1
                        self.reset()
            else:
                self.win = False
                self.state = GameState.in_menu
                answer = WIN_FAIL_TEXT[self.win]
                answer += '\n' + MENU_TEXT
                self.num_of_fails += 1
                self.reset()
        return answer
