class BoardAI:
    """
    The logic behind the decisions of the board moves, otherwise known as AI.

    """
    def __init__(self, board, symbol):
        """
        Initialization of the class.

        :param board: the board which is going to be used to take decisions
        :param symbol: the current board (used to identify fitness, because it is either positive or negative)

        :var board: a list of 9 str objects which all represent the board that is being held within the GUI.
        :var symbol: a str symbol, either 'X' or 'O'. represents the current turn.

        """
        self.board = board
        self.symbol = symbol


    def get_possibilities(self, board):
        """Get all the possibilities for the symbol that is defined by the class.
        for the board that is given.

        :param board list: Recieves a list with 'X', 'O' and '' corresponding
        to their location on a tic-tac-toe board.
        :return list: all the possible moves in a list.
        """

        possibilities = []

        # Creates a copy of the board so that the original board doesn't change.
        # Can also use a tuple.

        for i in range(len(board)):
            board_copy = board.copy()

            if board_copy[i] == '':
                board_copy[i] = self.symbol
                possibilities.append(board_copy)

        return possibilities

    def evaluate(self, board):
        """Evaluate a board.

        :param board list: Recieves a list with 'X', 'O' and '' corresponding
        to their location on a tic-tac-toe board.
        :return dict:
        fitness: a rating 'fitness' for the board, dependent to the symbol defined in the class initialization.
        board: the board that was argumented in the function call to ease readability when there are multiple results.

        """

        x1, o1, x2, o2 = 0, 0, 0, 0

        for i in range(3):

            # Compacts all possible lines in the board
            horizontal_board = [board[0+(i*3)], board[1+(i*3)], board[2+(i*3)]]
            vertical_board = [board[0+i], board[3+i], board[6+i]]
            diagonal1_board = [board[0], board[4], board[8]]
            diagonal2_board = [board[2], board[4], board[6]]
            lines = [horizontal_board, vertical_board, diagonal1_board, diagonal2_board]


            for line in lines:

                if line.count('') == 0:
                    if line.count('X') == 3:
                        return {
                            'fitness': float('inf') if self.symbol == 'X' else float('-inf'),
                            'board': board
                        }
                    if line.count('O') == 3:
                        return {
                            'fitness': float('-inf') if self.symbol == 'X' else float('inf'),
                            'board': board
                        }

                if line.count('') == 1:
                    if line.count('X') == 2:
                        x2 += 1
                    if line.count('O') == 2:
                        o2 += 1

                if line.count('') == 2:
                    if line.count('X') == 1:
                        x1 += 1
                    if line.count('O') == 1:
                        o1 += 1

        # Evaluation process
        x = (10 * x2 + x1)
        o = (10 * o2 + o1)
        # Returns fitness dependent on the symbol. If the symbol is 'O':
        # If good for 'X', it is positive.
        # If good for 'O', it is negative.

        return {
            'fitness': x - o if self.symbol == 'X' else o - x,
            'board': board
        }

    def best_move(self):
        """Get the best move.

        :return int: returns the index of the best position to add a symbol.
        """

        moves = []

        # Gets all possibilities and appends it to moves.
        for board in self.get_possibilities(self.board):
            moves.append(self.evaluate(board))

        # Sorts moves by key: fitness from higher to lower.
        moves.sort(key=lambda x: x['fitness'], reverse=True)

        # Gets the highest fitness move (because it was sorted by fitness) and stores it in move.
        move = moves[0]['board']

        # Inverts the symbols because we are going to simulate future moves.
        if self.symbol == 'X':
            self.symbol = 'O'
        elif self.symbol == 'O':
            self.symbol = 'X'

        # Rates a move ahead! (Also inverts the symbols, like done in the last piece of code.)
        for i, board in enumerate(moves):
            to_add = 0
            for j, possible_board in enumerate(self.get_possibilities(moves[i]['board'])):
                to_add += self.evaluate(possible_board)['fitness']
            moves[i]['fitness'] -= to_add

        # Sorts once more
        moves.sort(key=lambda x: x['fitness'], reverse=True)
        move = moves[0]['board']

        # Edge case
        if moves[0]['fitness'] == 110 and moves[1]['fitness'] == 110:
            move = moves[2]['board']

        # Gets the index of the new letter in the best move, so that it can get added.
        for i in range(len(move)):
            if self.board[i] != move[i]:
                return i