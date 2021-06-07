import copy
import random

AI_PLAYER = '1'
HUMAN_PLAYER = '2'
PLAYERS = [AI_PLAYER, HUMAN_PLAYER]
TWO_IN_A_ROW = 4
THREE_IN_A_ROW = 12
FOUR_IN_A_ROW = 100
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
        # check if valid move (available slot)
        if self.grid[startOfColumn + 5] != '0':
            print("Invalid Move")
            return
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

    def evalState(self):
        # Idea:
        # A weighted linear function, including features:
        # A 2 in a row = 4 (horizontally, vertically, or diagonally)
        # A 3 in a row = 12 ``
        # A 4 in a row = >> 100 ``
        # Pieces are better placed in the center columns and lower rows so:
        # A piece in the center column = 2
        # A piece on the left or right of the center column = 1
        # A piece on the lowest row = 3
        # A piece on the second lowest row = 2
        # A piece on the third lowest row = 1
        # Numbers are arbitrary and subject to change
        # For maximizing player (the AI) the numbers are added (wins with highest number)
        # For minimizing player (human) the numbers are subtracted (wins with lowest number)

        score = 0
        currGrid = self.grid

        # 2 in a row:
        # 1. HORIZONTALLY:
        for i in range(36):
            if currGrid[i] == AI_PLAYER and currGrid[i + 6] == AI_PLAYER:
                score += TWO_IN_A_ROW
            elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 6] == HUMAN_PLAYER:
                score -= TWO_IN_A_ROW
        # 2. Vertically
        for j in range(0, 36, 6):
            for i in range(4):
                if currGrid[i + j] == AI_PLAYER and currGrid[i + j + 1] == AI_PLAYER:
                    score += TWO_IN_A_ROW
                elif currGrid[i + j] == HUMAN_PLAYER and currGrid[i + 1 + j] == HUMAN_PLAYER:
                    score -= TWO_IN_A_ROW
        # 3. Positively sloped diagonals:
        # (don't consider the cases where the diagonal length is less than 4 as it is meaningless)

        for i in positiveDiagonalFor2:
            if currGrid[i] == AI_PLAYER and currGrid[i + 7] == AI_PLAYER:
                score += TWO_IN_A_ROW
            elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 7] == HUMAN_PLAYER:
                score -= TWO_IN_A_ROW
        # 4. Negatively sloped diagonals:

        for i in negativeDiagonalFor2:
            if currGrid[i] == AI_PLAYER and currGrid[i + 5] == AI_PLAYER:
                score += TWO_IN_A_ROW
            elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 5] == HUMAN_PLAYER:
                score -= TWO_IN_A_ROW

        # 3 in a row
        # 1. HORIZONTALLY:
        for i in range(29):
            if currGrid[i] == AI_PLAYER and currGrid[i + 6] == AI_PLAYER and currGrid[i + 12] == AI_PLAYER:
                score += THREE_IN_A_ROW
            elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 6] == HUMAN_PLAYER and currGrid[i + 12] == HUMAN_PLAYER:
                score -= 3
        # 2. Vertically
        for j in range(0, 36, 6):
            for i in range(4):
                if currGrid[i + j] == AI_PLAYER and currGrid[i + j + 1] == AI_PLAYER and currGrid[
                    i + j + 2] == AI_PLAYER:
                    score += THREE_IN_A_ROW
                elif currGrid[i + j] == HUMAN_PLAYER and currGrid[i + j + 1] == HUMAN_PLAYER \
                        and currGrid[i + j + 2] == HUMAN_PLAYER:
                    score -= THREE_IN_A_ROW
        # 3. Positively sloped diagonals:
        # (don't consider the cases where the diagonal length is less than 4 as it is meaningless)

        for i in positiveDiagonalFor3:
            if currGrid[i] == AI_PLAYER and currGrid[i + 7] == AI_PLAYER and currGrid[i + 14] == AI_PLAYER:
                score += THREE_IN_A_ROW
            elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 7] == HUMAN_PLAYER \
                    and currGrid[i + 14] == HUMAN_PLAYER:
                score -= THREE_IN_A_ROW
        # 4. Negatively sloped diagonals:
        for i in negativeDiagonalFor3:
            if currGrid[i] == AI_PLAYER and currGrid[i + 5] == AI_PLAYER and currGrid[i + 10] == AI_PLAYER:
                score += THREE_IN_A_ROW
            elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 5] == HUMAN_PLAYER \
                    and currGrid[i + 10] == HUMAN_PLAYER:
                score -= THREE_IN_A_ROW
        # 4 in a row
        score = self.countMatchingFours(score)

        # A piece on the center left or right
        for i in range(12, 18):
            if currGrid[i] == AI_PLAYER:
                score += 2
            elif currGrid[i] == HUMAN_PLAYER:
                score -= 2
        for i in range(30, 36):
            if currGrid[i] == AI_PLAYER:
                score += 2
            elif currGrid[i] == HUMAN_PLAYER:
                score -= 2
        # A piece in the center column
        for i in range(24, 30):
            if currGrid[i] == AI_PLAYER:
                score += 3
            elif currGrid[i] == HUMAN_PLAYER:
                score -= 3
        # A piece in the lowest row
        for i in range(0, 37, 6):
            if currGrid[i] == AI_PLAYER:
                score += 3
            elif currGrid[i] == HUMAN_PLAYER:
                score -= 3
        # A piece in the second lowest row
        for i in range(1, 38, 6):
            if currGrid[i] == AI_PLAYER:
                score += 2
            elif currGrid[i] == HUMAN_PLAYER:
                score -= 2
        # A piece in the third lowest row
        for i in range(2, 39, 6):
            if currGrid[i] == AI_PLAYER:
                score += 1
            elif currGrid[i] == HUMAN_PLAYER:
                score -= 1

        return score

    def countMatchingFours(self, score):
        currGrid = self.grid
        # 1. HORIZONTALLY:
        for i in range(23):
            if currGrid[i] == AI_PLAYER and currGrid[i + 6] == AI_PLAYER and currGrid[i + 12] == AI_PLAYER \
                    and currGrid[i + 18] == AI_PLAYER:
                score += FOUR_IN_A_ROW
            elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 6] == HUMAN_PLAYER and currGrid[i + 12] == HUMAN_PLAYER \
                    and currGrid[i + 18] == HUMAN_PLAYER:
                score -= FOUR_IN_A_ROW
        # 2. Vertically
        for j in range(0, 36, 6):
            for i in range(4):
                if currGrid[i + j] == AI_PLAYER and currGrid[i + j + 1] == AI_PLAYER and currGrid[
                    i + j + 2] == AI_PLAYER \
                        and currGrid[i + j + 3] == AI_PLAYER:
                    score += FOUR_IN_A_ROW
                elif currGrid[i + j] == HUMAN_PLAYER and currGrid[i + j + 1] == HUMAN_PLAYER \
                        and currGrid[i + j + 2] == HUMAN_PLAYER and currGrid[i + j + 3] == HUMAN_PLAYER:
                    score -= FOUR_IN_A_ROW
        # 3. Positively sloped diagonals:
        # (don't consider the cases where the diagonal length is less than 4 as it is meaningless)
        for i in positiveDiagonalIndices:
            if currGrid[i] == AI_PLAYER and currGrid[i + 7] == AI_PLAYER and currGrid[i + 14] == AI_PLAYER \
                    and currGrid[i + 21] == AI_PLAYER:
                score += FOUR_IN_A_ROW
            elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 7] == HUMAN_PLAYER \
                    and currGrid[i + 14] == HUMAN_PLAYER and currGrid[i + 21] == HUMAN_PLAYER:
                score -= FOUR_IN_A_ROW
        # 4. Negatively sloped diagonals:
        for i in negativeDiagonalIndices:
            if currGrid[i] == AI_PLAYER and currGrid[i + 5] == AI_PLAYER and currGrid[i + 10] == AI_PLAYER \
                    and currGrid[i + 15] == AI_PLAYER:
                score += FOUR_IN_A_ROW
            elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 5] == HUMAN_PLAYER \
                    and currGrid[i + 10] == HUMAN_PLAYER and currGrid[i + 15] == HUMAN_PLAYER:
                score -= FOUR_IN_A_ROW
        return score

    def eval(self):
        score = 0
        current_grid = self.grid
        number_of_connected = 0
        FOUR_CONNECTED = 100
        THREE_CONNECTED = 50
        TWO_CONNECTED = 20
        PLAYER_ONE = 1
        PLAYER_TWO = -1
        # Check Vertical Alignments
        for i in range(0, 6):
            cell_index = i * 6
            current_cell = current_grid[cell_index]
            while current_grid[cell_index] != '0':
                cell_index += 1
                if current_grid[cell_index] == current_cell:
                    number_of_connected += 1
                else:
                    number_of_connected = 0
                    current_cell = current_grid[cell_index]
            if current_grid[cell_index - 1] == '1':
                factor = PLAYER_ONE
            else:
                factor = PLAYER_TWO

            if number_of_connected >= 4:
                score += factor * (number_of_connected - 4 - 1) * FOUR_CONNECTED
            elif number_of_connected == 3:
                score += factor * THREE_CONNECTED
            elif number_of_connected == 2:
                score += factor * TWO_CONNECTED

        # Check Horizontal Alignments
        for i in range(0, 6):
            cell_index = i
            current_cell = current_grid[cell_index]
            while current_grid[cell_index] != '0':
                cell_index += 6
                if current_grid[cell_index] == current_cell:
                    number_of_connected += 1
                else:
                    number_of_connected = 0
                    current_cell = current_grid[cell_index]

            if current_grid[cell_index - 1] == '1':
                factor = PLAYER_ONE
            else:
                factor = PLAYER_TWO

            if number_of_connected >= 4:
                score += factor * (number_of_connected - 4 - 1) * FOUR_CONNECTED
            elif number_of_connected == 3:
                score += factor * THREE_CONNECTED
            elif number_of_connected == 2:
                score += factor * TWO_CONNECTED

        return

    def isTerminal(self):
        """
        returns boolean that indicates if the board is completely filled or not
        """
        for i in range(NUM_COLUMNS):
            if self.isValidMove(i):
                return False
            else:
                return True

    def isWinning(self, player):
        if self.isTerminal():
            score = self.countMatchingFours(0) // 100
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

grid = "200000100000210000000000110000122200000000"
gameState = GameState(grid, random.choice(PLAYERS), None)
gameState.printGrid()
print(gameState.evalState())
