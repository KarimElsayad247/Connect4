# GUI goes here

import pygame
import pygame_gui

APPLICATION_TITLE = 'Connect4'

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 900


GAME_HORIZONTAL_TILE_COUNT = 7
GAME_VERTICA_TILE_COUNT = 6
BOARD_START_X = 30
BOARD_START_Y = 60

# 7 horizontal tiles means width (700/7) = 100px for each tile
# thus radius of each is at max 100/2 = 50px
MAIN_RADIUS = 50
THICKNESS = 10
CIRCLE_MARGIN = THICKNESS + 30

GAME_AREA_WIDTH = (MAIN_RADIUS*2 + CIRCLE_MARGIN) * GAME_HORIZONTAL_TILE_COUNT
GAME_AREA_HEIGHT = (MAIN_RADIUS*2 + CIRCLE_MARGIN) * GAME_VERTICA_TILE_COUNT

COLUMN_WIDTH = GAME_AREA_WIDTH / GAME_HORIZONTAL_TILE_COUNT
COLUMN_HEIGHT = COLUMN_WIDTH

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
BLACK = (0,0,0)
WHITE = (255, 255, 255)

BACKGROUND_COLOR = DARK_TURQUOISE

PLAYER_COLORS = [RED, YELLOW]

class Circle:

    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.color = color

    def draw(self):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.r)

# create a 2d matrix of circles for the game board
board_circles = [[Circle(BOARD_START_X + 50 + (100 + CIRCLE_MARGIN)*i,
                         BOARD_START_Y + 50 + (100 + CIRCLE_MARGIN)*j, MAIN_RADIUS, GREY)
                 for i in range(GAME_HORIZONTAL_TILE_COUNT)]
                 for j in range(GAME_VERTICA_TILE_COUNT)]

# larger circles around the base circles that will give the illusion of edges
circle_edges = [[Circle(circle.x, circle.y, MAIN_RADIUS + THICKNESS, DARK_BLUE) for circle in row ] for row in board_circles]

# for now, I'll use a 2d list to represent the board logically
board_state = [[0 for i in range(GAME_HORIZONTAL_TILE_COUNT)] for j in range(GAME_VERTICA_TILE_COUNT)]

# variable that controls color of each inserted
current_player = 0


def processClick(x, y, player):
    i = int((y - BOARD_START_Y/2 ) // COLUMN_HEIGHT)
    j = int((x - BOARD_START_X/2) // COLUMN_WIDTH)
    print(f'clicked row {i}')
    print(f'clicked column {j}')

    board_state[i][j] = player
    board_circles[i][j].color = PLAYER_COLORS[player]



# must initialize pygame as program start
# this is just something to be done
pygame.init()

# The window inside which we put everything. Change width and height from the constants above
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# The UI manager handles calling the update, draw and event handling
# functions of all the UI elements we create and assign to it.
manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))

# the title of the window that appears in title bar
pygame.display.set_caption(APPLICATION_TITLE)

clock = pygame.time.Clock()

time_counter = 0
running = True

while running:

    time_delta = clock.tick(60) / 1000  # This variable is for gui manager
    time_counter += time_delta * 1000   # This variable is for animation and other timed events

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

        # Checking for a mouseclick on a tile
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            # Check If the position of mouse click is within border of Tile Area
            # No need to do any swapping otherwise
            if x < GAME_AREA_WIDTH and y < GAME_AREA_HEIGHT:
                processClick(event.pos[0], event.pos[1], current_player)
                current_player = not current_player

        manager.process_events(event)

    # specific to pygame_gui, must be called every loop to update UI
    manager.update(time_delta)

    # fill the screen with the background color before drawing anything else
    window.fill(BACKGROUND_COLOR)

    # Drawing game objects

    # draw the edges firs, because we want the circles to cover them
    for row in circle_edges:
        for edge in row:
            edge.draw()

    for row in board_circles:
        for circle in row:
            circle.draw()

    # called every loop to update visuals
    manager.draw_ui(window)
    pygame.display.update()

# quit application if somehow loop is escaped
pygame.quit()