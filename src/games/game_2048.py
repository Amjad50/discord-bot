from numpy.random import choice
import asyncio


class Game2048:

    def __init__(self, bot, player):
        self._bot = bot
        self._player = player
        self._board = [0] * 16
        self.score = 0
        self.add_new(2)  # adding new element.

    def __repr__(self):
        result = '+' + '-' * 7 + '+\n'

        for row in range(4):
            result += '|'
            for col in range(4):
                result += str(self._board[(row * 4) + col])
                result += '|'
            result += ('\n+' + '-' * 7 + '+\n')
        return result

    def add_new(self, times=1):
        free_places = [i for i in range(16) if self._board[i] == 0]
        for _ in range(times):
            if len(free_places) != 0:
                chosen = choice(free_places)
                self._board[chosen] = 2
                free_places.remove(chosen)
            else:
                raise RuntimeError("cannot add new_element because _board is full.")
