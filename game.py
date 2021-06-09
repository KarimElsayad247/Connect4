# GUI goes here
import math
import pygame
import pygame_gui
import minimax
import GameState

APPLICATION_TITLE = 'Connect4'

WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 700

GAME_HORIZONTAL_TILE_COUNT = 7
GAME_VERTICA_TILE_COUNT = 6
BOARD_START_X = 10
BOARD_START_Y = 10

# 7 horizontal tiles means width (700/7) = 100px for each tile
# thus radius of each is at max 100/2 = 50px
MAIN_RADIUS = 50
THICKNESS = 5
CIRCLE_MARGIN = THICKNESS + 10

COLUMN_WIDTH = MAIN_RADIUS * 2 + CIRCLE_MARGIN
COLUMN_HEIGHT = MAIN_RADIUS * 2 + CIRCLE_MARGIN

GAME_AREA_WIDTH = COLUMN_WIDTH * GAME_HORIZONTAL_TILE_COUNT
GAME_AREA_HEIGHT = COLUMN_HEIGHT * GAME_VERTICA_TILE_COUNT

print(GAME_AREA_WIDTH)
print(GAME_AREA_HEIGHT)
print(COLUMN_WIDTH)

# Colors
YELLOW = (250, 200, 3)
RED = (205, 28, 47)
BLUE = (29, 99, 245)
DARK_BLUE = (22, 86, 138)
DARK_TURQUOISE = (3, 54, 73)
GREY = (208, 208, 208)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BACKGROUND_COLOR = DARK_TURQUOISE

HUMAN = 1
AI = 2
PLAYER_COLORS = [GREY, RED, YELLOW]


class Circle:

    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.color = color

    def draw(self):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.r)


class Board:

    def __init__(self):
        # create a 2d matrix of circles for the game board
        self.board_circles = [[Circle(BOARD_START_X + 50 + (100 + CIRCLE_MARGIN) * i,
                                      BOARD_START_Y + 50 + (100 + CIRCLE_MARGIN) * j, MAIN_RADIUS, GREY)
                               for i in range(GAME_HORIZONTAL_TILE_COUNT)]
                              for j in range(GAME_VERTICA_TILE_COUNT)]

        # larger circles around the base circles that will give the illusion of edges
        self.circle_edges = [[Circle(circle.x, circle.y, MAIN_RADIUS + THICKNESS, DARK_BLUE) for circle in row]
                             for row in self.board_circles]

        # for now, I'll use a 2d list to represent the board logically
        self.board_state = [[0 for i in range(GAME_HORIZONTAL_TILE_COUNT)] for j in range(GAME_VERTICA_TILE_COUNT)]

        # height array that keeps the height of each column
        # useful for quickly inserting into column
        # the larger the number, the shorter the column
        # starts with all columns at value = 5
        self.column_heights = [GAME_VERTICA_TILE_COUNT - 1 for i in range(GAME_HORIZONTAL_TILE_COUNT)]


gameBoard = Board()

# variable that controls color of each inserted
current_player = HUMAN


def humanPlay(x, y, player, board):
    i = int((y - BOARD_START_Y / 2) // COLUMN_HEIGHT)
    j = int((x - BOARD_START_X / 2) // COLUMN_WIDTH)
    print(f'clicked row {i}')
    print(f'clicked column {j}')
    performMove(j, player, board)


# takes the 2d board and converts it into appropriate string format
def buildStateString(board):
    stringList = []
    for column in range(GAME_HORIZONTAL_TILE_COUNT):
        for row in range(GAME_VERTICA_TILE_COUNT - 1, -1, -1):
            stringList.append(str(board.board_state[row][column]))  # GameState wants strings
    return ''.join(stringList)


# returns the values used for the new column_heights array after modifying state
def calculateColumnHeights(board):
    heights = [GAME_VERTICA_TILE_COUNT - 1 for i in range(GAME_HORIZONTAL_TILE_COUNT)]
    for j in range(GAME_HORIZONTAL_TILE_COUNT):  # for each column
        for i in range(GAME_VERTICA_TILE_COUNT - 1, -1, -1):  # for each row in column starting from below
            if board.board_state[i][j] != 0:  # if state is not 0, then it's used
                heights[j] -= 1
    return heights


# returns a 2d list containing the new board state
# the string is the one usually used to represent a state
def buildBoardListFromString(stateString: str):
    board_list = [[0 for i in range(GAME_HORIZONTAL_TILE_COUNT)] for j in range(GAME_VERTICA_TILE_COUNT)]
    stringPointer = 0
    for j in range(GAME_HORIZONTAL_TILE_COUNT):
        for i in range(GAME_VERTICA_TILE_COUNT - 1, -1, -1):
            board_list[i][j] = int(stateString[stringPointer])  # from string to int since GUI uses ints for stuff
            stringPointer += 1
    return board_list


# returns the appropriate action for the AI to perform
# An integer between 0:6 representing column in which to insert
def aiPlay(board):
    # Converts current board state into appropriate format for minimax
    stateString = buildStateString(board)
    state = GameState.GameState(stateString, GameState.AI_PLAYER, None)
    print("score: " + str(state.eval()))
    k = 8
    minimax.resetDict()
    # calls either Minimax or MinimaxAlphaBeta based on result from dropdown
    if solveChoice == "MiniMax":
        decision = minimax.decisionMinimax(state, k)
    else:
        decision = minimax.decisionAlphaBeta(state, -math.inf, +math.inf, k)

    performMove(decision, current_player, gameBoard)


# Function that actually inserts a chip into a column
def performMove(j, player, board):
    if board.column_heights[j] >= 0:
        board.board_state[board.column_heights[j]][j] = player
        board.board_circles[board.column_heights[j]][j].color = PLAYER_COLORS[player]
        board.column_heights[j] -= 1
    else:
        print("can't insert here")
        # TODO: ERROR BOX

    print(buildStateString(board))


# takes a string representing a board state and changes relevant board variables
# to reflect said string
def modifyState(stateString: str):
    board = Board()
    board.board_state = buildBoardListFromString(stateString)
    for circle_row, state_row in zip(board.board_circles, board.board_state):
        for circle, state in zip(circle_row, state_row):
            circle.color = PLAYER_COLORS[state]
    board.column_heights = calculateColumnHeights(board)
    return board


# when board is filled, displays which player won and prompts user to close game or play again
def gameOver(board):
    # if the height list contains a number larger than -1 there are still moves possible
    for h in board.column_heights:
        if h > -1:
            return False
    return True


# must initialize pygame as program start
# this is just something to be done
pygame.init()

# The window inside which we put everything. Change width and height from the constants above
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# The UI manager handles calling the update, draw and event handling
# functions of all the UI elements we create and assign to it.
manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))


# for ease of creating rects ordered properly for side panel
def getRect(order):
    return pygame.Rect((850, (50 * order + 50)), (200, 50))


inputTextFieldRect = getRect(0)
inputTextField = pygame_gui.elements.UITextEntryLine(
    relative_rect=inputTextFieldRect, manager=manager)
inputTextField.set_allowed_characters(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
inputTextField.set_text_length_limit(1)

solveChoiceRect = getRect(1)
solveChoice = pygame_gui.elements.UIDropDownMenu(
    ["MiniMax", "AlphaBeta"], "MiniMax",
    relative_rect=solveChoiceRect, manager=manager)

confirmButtonRect = getRect(2)
confirmButton = pygame_gui.elements.UIButton(
    relative_rect=confirmButtonRect, text="Confirm", manager=manager)

restartButtonRect = getRect(3)
restartButton = pygame_gui.elements.UIButton(
    relative_rect=restartButtonRect, text="Restart", manager=manager)

# the title of the window that appears in title bar
pygame.display.set_caption(APPLICATION_TITLE)

clock = pygame.time.Clock()

time_counter = 0
running = True

while running:

    time_delta = clock.tick(60) / 1000  # This variable is for gui manager
    time_counter += time_delta * 1000  # This variable is for animation and other timed events

    # This comment is copies from the previous project in case anyone forgot why some stuff are important
    # a game loop consists of 2 main phases: update phase, and draw phase
    # in update phase we perform all modifications, then in draw phase we
    # show the effect of those modifications.
    # Hence, responding to events happens in update phase, in which we will do
    # things like restarting board, solving a problem, and so on.

    # check the event queue for events, such as quit or click
    # If the program doesn't process the event queue, the OS considers the app frozen and app crashes
    events = pygame.event.get()

    # processing the event queue
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        # specific to the UI library. all events related to pygame_gui go here
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == restartButton:
                    gameBoard = modifyState("000000000000000000000000000000000000000000")

        # ai will move only on its turn.
        if current_player == AI:
            aiPlay(gameBoard)
            current_player = HUMAN

        # Checking for a mouseclick on a tile
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if not gameOver(gameBoard):
                if current_player == HUMAN:
                    # Check If the position of mouse click is within border of Tile Area
                    # No need to do any swapping otherwise
                    print(f'clicked {event.pos[0]}, {event.pos[1]}')
                    if x < GAME_AREA_WIDTH and y < GAME_AREA_HEIGHT:
                        humanPlay(event.pos[0], event.pos[1], current_player, gameBoard)
                        current_player = AI
            else:
                print(f'Game Over! press restart when available')

        manager.process_events(event)

    # specific to pygame_gui, must be called every loop to update UI
    manager.update(time_delta)

    # fill the screen with the background color before drawing anything else
    window.fill(BACKGROUND_COLOR)

    # Drawing game objects

    # draw the edges firs, because we want the circles to cover them
    for row in gameBoard.circle_edges:
        for edge in row:
            edge.draw()

    for row in gameBoard.board_circles:
        for circle in row:
            circle.draw()

    # called every loop to update visuals
    manager.draw_ui(window)
    pygame.display.update()

# quit application if somehow loop is escaped
pygame.quit()
