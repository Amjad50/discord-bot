from numpy.random import choice
import asyncio


class Game2048:

    def __init__(self, bot, player, channel):
        self._bot = bot
        self._player = player
        self._channel = channel
        self.score = 0
        self.moves = 0
        self.running = False
        self._board = [0] * 16
        self.score = 0
        self.__range4 = [0, 1, 2, 3]
        self.directions_config = {
            'up': {
                'rows_first': True,
                'rows': range(1, 4),
                'cols': range(4),
                'check_func': lambda current_pos: current_pos > 3,
                'increment_val': -4
            },
            'down': {
                'rows_first': True,
                'rows': range(2, -1, -1),
                'cols': range(4),
                'check_func': lambda current_pos: current_pos < 12,
                'increment_val': +4
            },
            'right': {
                'rows_first': False,
                'rows': range(4),
                'cols': range(2, -1, -1),
                'check_func': lambda current_pos: (current_pos % 4) != 3,
                'increment_val': +1
            },
            'left': {
                'rows_first': False,
                'rows': range(4),
                'cols': range(1, 4),
                'check_func': lambda current_pos: (current_pos % 4) != 0,
                'increment_val': -1
            }
        }
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
        print("adding in: ", end='')  # debugging
        for _ in range(times):
            if len(free_places) != 0:
                chosen = choice(free_places)
                self._board[chosen] = 2
                free_places.remove(chosen)
                print(chosen, end=' ')  # debugging
            else:
                raise RuntimeError("cannot add new_element because _board is full.")
        print()  #debugging

    def move(self, direction):
        try:
            direction_config = self.directions_config[direction]
        except KeyError:
            raise ValueError("'direction' argument must be 'up', 'down', 'right' or 'left'")

        def move_i():
            if self._board[index] != 0:
                current_pos = index  # save the initial position
                upgrade = False

                while direction_config['check_func'](current_pos):

                    # if another element exists
                    if self._board[current_pos + direction_config['increment_val']]:

                        # if they have the same val
                        if self._board[current_pos + direction_config['increment_val']] == \
                                self._board[index]:
                            upgrade = True
                            current_pos += direction_config['increment_val']
                        break
                    else:
                        current_pos += direction_config['increment_val']

                if current_pos != index:
                    if upgrade:
                        self._board[current_pos] *= 2
                    else:
                        self._board[current_pos] = self._board[index]
                    self._board[index] = 0

        if direction_config['rows_first']:
            for row in direction_config['rows']:
                for col in direction_config['cols']:
                    index = (row * 4) + col
                    move_i()
        else:
            for col in direction_config['cols']:
                for row in direction_config['rows']:
                    index = (row * 4) + col
                    move_i()

        self.add_new()

    @asyncio.coroutine
    async def run(self):
        emojis = ["⬆", "⬇", "➡", "⬅"]
        self.message = await self._bot.send_message(self._channel, "starting game...")
        self.running = True

        while self.running:
            await self._bot.edit_message(self.message, "score: {0}\nmoves: {1}\n{2}".format(
                self.score, self.moves, self
            ))

            await self._bot.add_reaction(self.message, emoji="⬆")
            await self._bot.add_reaction(self.message, emoji="⬇")
            await self._bot.add_reaction(self.message, emoji="➡")
            await self._bot.add_reaction(self.message, emoji="⬅")

            respond = await self._bot.wait_for_reaction(message=self.message,
                                                        check=lambda r,
                                                                     u: u == self._player and r.emoji in emojis)
            if self.running:
                if respond.reaction.emoji == "⬆":
                    self.move('up')
                elif respond.reaction.emoji == "⬇":
                    self.move('down')
                elif respond.reaction.emoji == "➡":
                    self.move('right')
                elif respond.reaction.emoji == "⬅":
                    self.move('left')
                await self._bot.remove_reaction(self.message, respond.reaction.emoji, self._player)
                self.moves += 1

    @asyncio.coroutine
    async def stop(self):
        self.running = False
        await self._bot.send_message(self._channel,
                                     "game stopped with:\nscore: {0}\nmoves: {1}".format(
                                         self.score, self.moves
                                     ))
