import copy


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
        newGrid = newGrid[:startOfColumn] + str(self.player) + newGrid[startOfColumn + 1:]
        # check if it's player 1 or player 2 move
        player = 1 if self.player == 2 else 2
        return GameState(newGrid, player, move)

    def expand(self):
        children = []
        for i in range(0, 7):
            children.append(self.makeMove(i))
        return children

    def heuristic(self):
        # TODO: write an admissible heuristic function
        return

