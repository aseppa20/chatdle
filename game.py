from copy import deepcopy

class game:
    correct_answer: str
    max_guesses: int
    guessed = set()
    state_hash: int
    # Game state describes all the guesses done, if game runs
    _game_state = {
        "_guesses": 0,
        "_max_guesses": int,
        "_running": False
    }

    def __init__(self, correct_answer: str, max_guesses: int = -1) -> None:
        self.reset(correct_answer, max_guesses)

    def reset(self, correct_answer: str, max_guesses: int = -1):
        self.correct_answer = correct_answer
        self._game_state = {
            "_guesses": 0,
            "_max_guesses": int,
            "_running": False
        }
        self.max_guesses = max_guesses
        self._game_state["_max_guesses"] = max_guesses
        self._game_state["_running"] = True
        self.guessed = set()


    def _check_answer(self, guess: str) -> dict:
        answer_dict = {
            'correct': False,
            'positions': []
        }

        if guess == self.correct_answer:
            answer_dict['correct'] = True
            for _ in range(len(self.correct_answer)):
                answer_dict['positions'].append("True")
            return answer_dict
        
        counted_letters_correct_answer = {}
        counted_letters_guess = {}

        for char in self.correct_answer:
            if char in counted_letters_correct_answer:
                counted_letters_correct_answer[char] += 1
            else:
                counted_letters_correct_answer[char] = 1
        
        for char in guess:
            if char in counted_letters_guess:
                counted_letters_guess[char] += 1
            else:
                counted_letters_guess[char] = 1

        for i, char in enumerate(guess):
            if self.correct_answer.find(char) == -1:
                answer_dict['positions'].append("False")
            elif self.correct_answer[i] == char:
                answer_dict['positions'].append("True")
            else:
                if counted_letters_correct_answer[char] >= counted_letters_guess[char]:
                    answer_dict['positions'].append("Partial")
                else:
                    answer_dict['positions'].append("False")
        
        return answer_dict
    
    def guess(self, guess) -> tuple:
        if not (self.max_guesses == -1 or len(self.guessed) < self.max_guesses):
            self._game_state["_running"] = False
            return ("No guesses left", None)
        
        if len(guess) != len(self.correct_answer):
            return ("Guess is not of a correct length (No guesses used)", None)
        
        if guess in self.guessed:
            return ("Duplicate guess, try again. (No guesses used)", None)
        
        self.guessed.add(guess)

        answer = self._check_answer(guess)
        self._game_state[guess] = answer["positions"]
    
        if answer['correct']:
            self._game_state["_running"] = False
            return (f"CORRECT! You got it in {len(self.guessed)} guesses!", deepcopy(answer['positions']))
        else:
            if (guess == self.max_guesses):
                self._game_state["_running"] = False
                print(f"Incorrect. Game over! The correct answer was: {self.correct_answer}", deepcopy(answer['positions']))
            return (f"INCORRECT! Try again!", deepcopy(answer['positions']))
        
    def get_game_state(self) -> dict:
        self._game_state["_guesses"] = len(self.guessed)
        return self._game_state

    def _hash_state(self) -> None:
        self.state_hash = hash(self._game_state, self.correct_answer)
