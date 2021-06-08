import copy
import random
import timeit

AI_PLAYER = '2'
HUMAN_PLAYER = '1'

NUM_COLUMNS = 7


class GameState:
    """ GameState class
        player : player who played the current move
        grid : representation of the grid as string
        0 for available slot
        1 for player one slot
        2 for player two slot
        move : move that caused the current state
    """

    def __init__(self, grid, player, move):
        self.grid = grid
        self.player = player
        self.move = move

    def makeMove(self, move):
        startOfColumn = move * 6
        newGrid = copy.copy(self.grid)

        # get the current available cell
        while newGrid[startOfColumn] != '0' and startOfColumn < (move * 6) + 7:
            startOfColumn += 1
        newGrid = newGrid[:startOfColumn] + self.player + newGrid[startOfColumn + 1:]

        # check if it's player 1 or player 2 move
        player = AI_PLAYER if self.player == HUMAN_PLAYER else HUMAN_PLAYER
        return GameState(newGrid, player, move)

    def getChildren(self):
        children = []
        for i in range(0, 7):
            children.append(self.makeMove(i))
        return children

    # returns whither a move is valid for the purpose of creating a valid actions list
    def isValidMove(self, move):
        if self.grid[move * 6 + 5] == '0':
            return True
        else:
            return False

    #     # PLAYERS = [AI_PLAYER, HUMAN_PLAYER]
    # # TWO_IN_A_ROW = 4
    # # THREE_IN_A_ROW = 12
    # # FOUR_IN_A_ROW = 100

    # We didn't use the following function; we used eval instead, which implements the same heuristic with an algorithm
    # like greedy first algorithm
    # def evalState(self):
    #     # Idea:
    #     # A weighted linear function, including features:
    #     # A 2 in a row = 4 (horizontally, vertically, or diagonally)
    #     # A 3 in a row = 12 ``
    #     # A 4 in a row = >> 100 ``
    #     # Pieces are better placed in the center columns and lower rows so:
    #     # A piece in the center column = 2
    #     # A piece on the left or right of the center column = 1
    #     # A piece on the lowest row = 3
    #     # A piece on the second lowest row = 2
    #     # A piece on the third lowest row = 1
    #     # Numbers are arbitrary and subject to change
    #     # For maximizing player (the AI) the numbers are added (wins with highest number)
    #     # For minimizing player (human) the numbers are subtracted (wins with lowest number)
    #
    #     score = 0
    #     currGrid = self.grid
    #     # 2 in a row:
    #     # 1. HORIZONTALLY:
    #     for i in range(36):
    #         if currGrid[i] == AI_PLAYER and currGrid[i + 6] == AI_PLAYER:
    #             score += TWO_IN_A_ROW
    #         elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 6] == HUMAN_PLAYER:
    #             score -= TWO_IN_A_ROW
    #     # 2. Vertically
    #     for j in range(0, 36, 6):
    #         for i in range(4):
    #             if currGrid[i + j] == AI_PLAYER and currGrid[i + j + 1] == AI_PLAYER:
    #                 score += TWO_IN_A_ROW
    #             elif currGrid[i + j] == HUMAN_PLAYER and currGrid[i + 1 + j] == HUMAN_PLAYER:
    #                 score -= TWO_IN_A_ROW
    #     # 3. Positively sloped diagonals:
    #     # (don't consider the cases where the diagonal length is less than 4 as it is meaningless)
    #
    #     for i in positiveDiagonalFor2:
    #         if currGrid[i] == AI_PLAYER and currGrid[i + 7] == AI_PLAYER:
    #             score += TWO_IN_A_ROW
    #         elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 7] == HUMAN_PLAYER:
    #             score -= TWO_IN_A_ROW
    #     # 4. Negatively sloped diagonals:
    #
    #     for i in negativeDiagonalFor2:
    #         if currGrid[i] == AI_PLAYER and currGrid[i + 5] == AI_PLAYER:
    #             score += TWO_IN_A_ROW
    #         elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 5] == HUMAN_PLAYER:
    #             score -= TWO_IN_A_ROW
    #
    #     # 3 in a row
    #     # 1. HORIZONTALLY:
    #     for i in range(29):
    #         if currGrid[i] == AI_PLAYER and currGrid[i + 6] == AI_PLAYER and currGrid[i + 12] == AI_PLAYER:
    #             score += THREE_IN_A_ROW
    #         elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 6] == HUMAN_PLAYER and currGrid[i + 12] == HUMAN_PLAYER:
    #             score -= 3
    #     # 2. Vertically
    #     for j in range(0, 36, 6):
    #         for i in range(4):
    #             if currGrid[i + j] == AI_PLAYER and currGrid[i + j + 1] == AI_PLAYER \
    #                     and currGrid[i + j + 2] == AI_PLAYER:
    #                 score += THREE_IN_A_ROW
    #             elif currGrid[i + j] == HUMAN_PLAYER and currGrid[i + j + 1] == HUMAN_PLAYER \
    #                     and currGrid[i + j + 2] == HUMAN_PLAYER:
    #                 score -= THREE_IN_A_ROW
    #     # 3. Positively sloped diagonals:
    #     # (don't consider the cases where the diagonal length is less than 4 as it is meaningless)
    #
    #     for i in positiveDiagonalFor3:
    #         if currGrid[i] == AI_PLAYER and currGrid[i + 7] == AI_PLAYER and currGrid[i + 14] == AI_PLAYER:
    #             score += THREE_IN_A_ROW
    #         elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 7] == HUMAN_PLAYER \
    #                 and currGrid[i + 14] == HUMAN_PLAYER:
    #             score -= THREE_IN_A_ROW
    #     # 4. Negatively sloped diagonals:
    #     for i in negativeDiagonalFor3:
    #         if currGrid[i] == AI_PLAYER and currGrid[i + 5] == AI_PLAYER and currGrid[i + 10] == AI_PLAYER:
    #             score += THREE_IN_A_ROW
    #         elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 5] == HUMAN_PLAYER \
    #                 and currGrid[i + 10] == HUMAN_PLAYER:
    #             score -= THREE_IN_A_ROW
    #     # 4 in a row
    #     score = self.countMatchingFours(score)
    #
    #     # A piece on the center left or right
    #     for i in range(12, 18):
    #         if currGrid[i] == AI_PLAYER:
    #             score += 2
    #         elif currGrid[i] == HUMAN_PLAYER:
    #             score -= 2
    #     for i in range(30, 36):
    #         if currGrid[i] == AI_PLAYER:
    #             score += 2
    #         elif currGrid[i] == HUMAN_PLAYER:
    #             score -= 2
    #     # A piece in the center column
    #     for i in range(24, 30):
    #         if currGrid[i] == AI_PLAYER:
    #             score += 3
    #         elif currGrid[i] == HUMAN_PLAYER:
    #             score -= 3
    #     # A piece in the lowest row
    #     for i in range(0, 37, 6):
    #         if currGrid[i] == AI_PLAYER:
    #             score += 3
    #         elif currGrid[i] == HUMAN_PLAYER:
    #             score -= 3
    #     # A piece in the second lowest row
    #     for i in range(1, 38, 6):
    #         if currGrid[i] == AI_PLAYER:
    #             score += 2
    #         elif currGrid[i] == HUMAN_PLAYER:
    #             score -= 2
    #     # A piece in the third lowest row
    #     for i in range(2, 39, 6):
    #         if currGrid[i] == AI_PLAYER:
    #             score += 1
    #         elif currGrid[i] == HUMAN_PLAYER:
    #             score -= 1
    #
    #     return score
    #

    def eval(self):
        score = 0
        current_grid = self.grid
        FOUR_CONNECTED = [-4500, 4000]
        THREE_CONNECTED = [-500, 500]
        TWO_CONNECTED = [-100, 100]
        PLAYER_ONE = 0
        PLAYER_TWO = 1
        # Check Vertical Alignments
        for i in range(0, 7):
            number_of_connected = 0
            cell_index = i * 6
            current_cell = current_grid[cell_index]
            j = cell_index
            while j <= (i * 6) + 5 and current_grid[j] != '0':
                if current_grid[j] == current_cell:
                    number_of_connected += 1
                else:
                    if number_of_connected >= 4:
                        factor = PLAYER_ONE if current_grid[j - 1] == '1' else PLAYER_TWO
                        score += (number_of_connected - 3) * FOUR_CONNECTED[factor]
                    number_of_connected = 1
                    current_cell = current_grid[j]
                j += 1

            if current_grid[j - 1] == '1':
                factor = PLAYER_ONE
            else:
                factor = PLAYER_TWO

            if number_of_connected >= 4:
                score += (number_of_connected - 3) * FOUR_CONNECTED[factor]
            elif number_of_connected == 3 and j < (i * 6) + 6:
                score += THREE_CONNECTED[factor]
            elif number_of_connected == 2 and j < (i * 6) + 5:
                score += TWO_CONNECTED[factor]

        # Check Horizontal Alignments
        for i in range(0, 6):
            number_of_connected = 1
            cell_index = i
            current_cell = current_grid[cell_index]
            for j in range(i + 6, i + 37, 6):
                if current_grid[j] == current_cell and current_grid[j] != '0':
                    number_of_connected += 1
                else:
                    factor = PLAYER_ONE if current_grid[j - 6] == '1' else PLAYER_TWO
                    if 1 < number_of_connected < 4:
                        if checkRedundancy(current_grid, number_of_connected, i, j, current_grid[j - 6]):
                            if number_of_connected == 3:
                                score += THREE_CONNECTED[factor]
                            elif number_of_connected == 2:
                                score += TWO_CONNECTED[factor]
                    elif number_of_connected >= 4:
                        score += (number_of_connected - 3) * FOUR_CONNECTED[factor]
                    number_of_connected = 1
                    current_cell = current_grid[j]

        positiveDiagonalIndicesStarts = [0, 1, 2, 6, 12, 18]
        positiveDiagonalIndicesEnd = [35, 29, 23, 41, 40, 39]
        # Check Positive Diagonal Alignments
        for i in range(0, 6):
            number_of_connected = 0
            start = positiveDiagonalIndicesStarts[i]
            limit = positiveDiagonalIndicesEnd[i]
            cell_index = start
            current_cell = current_grid[cell_index]
            j = start
            while j <= limit:
                if current_grid[j] == current_cell and current_grid[j] != '0':
                    number_of_connected += 1
                else:
                    factor = PLAYER_ONE if current_grid[j - 7] == '1' else PLAYER_TWO
                    if 1 < number_of_connected < 4:
                        if checkRedundancyPositive(current_grid, number_of_connected,
                                                   i, j, current_grid[j - 7], start, limit):
                            if number_of_connected == 3:
                                score += THREE_CONNECTED[factor]
                            elif number_of_connected == 2:
                                score += TWO_CONNECTED[factor]
                    elif number_of_connected >= 4:
                        score += (number_of_connected - 3) * FOUR_CONNECTED[factor]
                    number_of_connected = 1
                    current_cell = current_grid[j]
                j += 7

        negativeDiagonalIndicesStarts = [36, 37, 38, 30, 24, 18]
        negativeDiagonalIndicesEnd = [11, 17, 23, 5, 4, 3]
        # Check Negative Diagonal Alignments
        for i in range(0, 6):
            number_of_connected = 0
            start = negativeDiagonalIndicesStarts[i]
            limit = negativeDiagonalIndicesEnd[i]
            cell_index = start
            current_cell = current_grid[cell_index]
            j = start
            while j >= limit:
                if current_grid[j] == current_cell and current_grid[j] != '0':
                    number_of_connected += 1
                else:
                    if 1 < number_of_connected < 4:
                        factor = PLAYER_ONE if current_grid[j + 5] == '1' else PLAYER_TWO
                        if checkRedundancyNegative(current_grid, number_of_connected,
                                                   i, j, current_grid[j + 5], start, limit):
                            if number_of_connected == 3:
                                score += THREE_CONNECTED[factor]
                            elif number_of_connected == 2:
                                score += TWO_CONNECTED[factor]
                    elif number_of_connected >= 4:
                        factor = PLAYER_ONE if current_grid[j + 5] == '1' else PLAYER_TWO
                        score += (number_of_connected - 3) * FOUR_CONNECTED[factor]
                    number_of_connected = 1
                    current_cell = current_grid[j]
                j -= 5
        # add slight bias towards center columns and lower rows (slightly better possibility for a win)
        HIGH_PRIORITY = 3
        MEDIUM_PRIORITY = 2
        LOW_PRIORITY = 1
        # A piece on the center left or right
        for i in range(12, 18):
            if current_grid[i] == AI_PLAYER:
                score += MEDIUM_PRIORITY
            elif current_grid[i] == HUMAN_PLAYER:
                score -= MEDIUM_PRIORITY
        for i in range(30, 36):
            if current_grid[i] == AI_PLAYER:
                score += MEDIUM_PRIORITY
            elif current_grid[i] == HUMAN_PLAYER:
                score -= MEDIUM_PRIORITY
        # A piece in the center column
        for i in range(24, 30):
            if current_grid[i] == AI_PLAYER:
                score += HIGH_PRIORITY
            elif current_grid[i] == HUMAN_PLAYER:
                score -= HIGH_PRIORITY
        # A piece in the lowest row
        for i in range(0, 37, 6):
            if current_grid[i] == AI_PLAYER:
                score += HIGH_PRIORITY
            elif current_grid[i] == HUMAN_PLAYER:
                score -= HIGH_PRIORITY
        # A piece in the second lowest row
        for i in range(1, 38, 6):
            if current_grid[i] == AI_PLAYER:
                score += MEDIUM_PRIORITY
            elif current_grid[i] == HUMAN_PLAYER:
                score -= MEDIUM_PRIORITY
        # A piece in the third lowest row
        for i in range(2, 39, 6):
            if current_grid[i] == AI_PLAYER:
                score += LOW_PRIORITY
            elif current_grid[i] == HUMAN_PLAYER:
                score -= LOW_PRIORITY
        return score

    def countMatchingFours(self):
        if self.isTerminal():
            positiveDiagonalIndices = [0, 1, 2, 6, 7, 8, 12, 13, 14, 18, 19, 20]
            negativeDiagonalIndices = [3, 4, 5, 9, 10, 11, 15, 16, 17, 21, 22, 23]
            positiveDiagonalFor3 = copy.copy(positiveDiagonalIndices)
            positiveDiagonalFor3.extend([9, 15, 21, 25, 26, 27])
            negativeDiagonalFor3 = copy.copy(negativeDiagonalIndices)
            negativeDiagonalFor3.extend([8, 14, 20, 26, 27, 28])
            positiveDiagonalFor2 = copy.copy(positiveDiagonalFor3)
            positiveDiagonalFor2.extend([16, 22, 28, 32, 33, 34])
            negativeDiagonalFor2 = copy.copy(negativeDiagonalFor3)
            negativeDiagonalFor2.extend([13, 19, 25, 31, 32, 33])
            currGrid = self.grid
            score = 0
            # 1. HORIZONTALLY:
            for i in range(23):
                if currGrid[i] == AI_PLAYER and currGrid[i + 6] == AI_PLAYER and currGrid[i + 12] == AI_PLAYER \
                        and currGrid[i + 18] == AI_PLAYER:
                    score += 1
                elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 6] == HUMAN_PLAYER \
                        and currGrid[i + 12] == HUMAN_PLAYER and currGrid[i + 18] == HUMAN_PLAYER:
                    score -= 1
            # 2. Vertically
            for j in range(0, 36, 6):
                for i in range(4):
                    if currGrid[i + j] == AI_PLAYER and currGrid[i + j + 1] == AI_PLAYER and currGrid[
                        i + j + 2] == AI_PLAYER \
                            and currGrid[i + j + 3] == AI_PLAYER:
                        score += 1
                    elif currGrid[i + j] == HUMAN_PLAYER and currGrid[i + j + 1] == HUMAN_PLAYER \
                            and currGrid[i + j + 2] == HUMAN_PLAYER and currGrid[i + j + 3] == HUMAN_PLAYER:
                        score -= 1
            # 3. Positively sloped diagonals:
            # (don't consider the cases where the diagonal length is less than 4 as it is meaningless)
            for i in positiveDiagonalIndices:
                if currGrid[i] == AI_PLAYER and currGrid[i + 7] == AI_PLAYER and currGrid[i + 14] == AI_PLAYER \
                        and currGrid[i + 21] == AI_PLAYER:
                    score += 1
                elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 7] == HUMAN_PLAYER \
                        and currGrid[i + 14] == HUMAN_PLAYER and currGrid[i + 21] == HUMAN_PLAYER:
                    score -= 1
            # 4. Negatively sloped diagonals:
            for i in negativeDiagonalIndices:
                if currGrid[i] == AI_PLAYER and currGrid[i + 5] == AI_PLAYER and currGrid[i + 10] == AI_PLAYER \
                        and currGrid[i + 15] == AI_PLAYER:
                    score += 1
                elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 5] == HUMAN_PLAYER \
                        and currGrid[i + 10] == HUMAN_PLAYER and currGrid[i + 15] == HUMAN_PLAYER:
                    score -= 1
            return score
        return 0

    def isTerminal(self):
        """
        returns boolean that indicates if the board is completely filled or not
        """
        for i in range(NUM_COLUMNS):
            if self.isValidMove(i):
                return False
        return True

    def isWinning(self, player):
        if self.isTerminal():
            score = self.countMatchingFours()
            print("Final score is " + str(score))
            if (score > 0 and player == AI_PLAYER) or (score < 0 and player == HUMAN_PLAYER):
                return True
        return False  # other player is winning or draw or not terminal yet

    def printGrid(self):
        for i in range(6):
            for x in range(7):
                print(self.grid[x * 6 + 5 - i], end=" ")
            print()
        print()


def checkRedundancy(state, Number, i, j, cell):
    undesired_cell = '1' if cell == '2' else '2'
    if Number == 2:
        left_one = j - (3 * 6)
        left_two = j - (4 * 6)
        right_one = j
        right_two = j + 6
        check_left_one = left_one >= 0 and state[left_one] != undesired_cell
        check_left_two = left_two >= 0 and state[left_two] != undesired_cell
        check_right_one = right_one <= 41 and state[right_one] != undesired_cell
        check_right_two = right_two <= 41 and state[right_two] != undesired_cell
        return (check_left_one and check_left_two) or \
               (check_left_one and check_right_one) or \
               (check_right_two and check_right_one)
        pass
    elif Number == 3:
        left_one = j - 4 * 6
        right_one = j
        check_left_one = left_one >= 0 and state[left_one] != undesired_cell
        check_right_one = right_one <= 41 and state[right_one] != undesired_cell
        return check_left_one or check_right_one


def checkRedundancyPositive(state, Number, i, j, cell, start, limit):
    undesired_cell = '1' if cell == '2' else '2'
    if Number == 2:
        left_one = j - 21
        left_two = j - 28
        right_one = j
        right_two = j + 7
        check_left_one = left_one >= start and state[left_one] != undesired_cell
        check_left_two = left_two >= start and state[left_two] != undesired_cell
        check_right_one = right_one <= limit and state[right_one] != undesired_cell
        check_right_two = right_two <= limit and state[right_two] != undesired_cell
        return (check_left_one and check_left_two) or \
               (check_left_one and check_right_one) or \
               (check_right_two and check_right_one)
        pass
    elif Number == 3:
        left_one = j - 28
        right_one = j
        check_left_one = left_one >= start and state[left_one] != undesired_cell
        check_right_one = right_one <= limit and state[right_one] != undesired_cell
        return check_left_one or check_right_one


def checkRedundancyNegative(state, Number, i, j, cell, start, limit):
    undesired_cell = '1' if cell == '2' else '2'
    if Number == 2:
        left_one = j
        left_two = j - 5
        right_one = j + 15
        right_two = j + 20
        check_left_one = left_one >= limit and state[left_one] != undesired_cell
        check_left_two = left_two >= limit and state[left_two] != undesired_cell
        check_right_one = right_one <= start and state[right_one] != undesired_cell
        check_right_two = right_two <= start and state[right_two] != undesired_cell
        return (check_left_one and check_left_two) or \
               (check_left_one and check_right_one) or \
               (check_right_two and check_right_one)
        pass
    elif Number == 3:
        left_one = j
        right_one = j + 20
        check_left_one = left_one >= limit and state[left_one] != undesired_cell
        check_right_one = right_one <= start and state[right_one] != undesired_cell
        return check_left_one or check_right_one

# newGrid = "0" * 42
# gameState = GameState(newGrid, random.choice(PLAYERS), None)
# printGrid(gameState.grid)
# print(gameState.evalState())
#
# gameState = gameState.makeMove(5)
# printGrid(gameState.grid)
# print(gameState.evalState())
#
# gameState = gameState.makeMove(5)
# printGrid(gameState.grid)
# print(gameState.evalState())
#
# gameState = gameState.makeMove(4)
# printGrid(gameState.grid)
# print(gameState.evalState())
#
# gameState = gameState.makeMove(5)
# printGrid(gameState.grid)
# print(gameState.evalState())
#
# gameState = gameState.makeMove(4)
# printGrid(gameState.grid)
# print(gameState.evalState())
#
# gameState = gameState.makeMove(5)
# printGrid(gameState.grid)
# print(gameState.evalState())
#
# gameState = gameState.makeMove(1)
# printGrid(gameState.grid)
# print(gameState.evalState())
#
# gameState = gameState.makeMove(2)
# printGrid(gameState.grid)
# print(gameState.evalState())
#
# gameState = gameState.makeMove(2)
# printGrid(gameState.grid)
# print(gameState.evalState())
#
# gameState = gameState.makeMove(0)
# printGrid(gameState.grid)
# print(gameState.evalState())
# print(gameState.grid)

# grid = "112220110000211000222220000000000000222000"
# gameState = GameState(grid, random.choice(PLAYERS), None)
# gameState.printGrid()
# print(gameState.eval())
