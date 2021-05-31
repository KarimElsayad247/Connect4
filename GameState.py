import copy


class GameState:
    def __init__(self, grid, player, move):
        self.grid = grid
        self.player = player
        self.move = move

    def makeMove(self, move):
        current_cell = move * 6
        newGrid = copy.copy(self.grid)
        while newGrid[current_cell] != '0' and current_cell < (move * 6) + 7:
            current_cell += 1
        newGrid = newGrid[:current_cell] + str(self.player) + newGrid[current_cell + 1:]
        player = 1 if self.player == 2 else 2
        return GameState(newGrid, player, move)


y = ''
for i in range(42):
    y += '0'
x = GameState(y, 1, 0)
y = x.makeMove(5)
print(y.grid)
z = y.makeMove(5)
print(z.grid)
