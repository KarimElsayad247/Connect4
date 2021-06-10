# Algorithms go here
import GameState
import math
import random
from time import sleep
from ete3 import Tree, TreeStyle, TextFace, add_face_to_node

"""
Karim Elsayed ID.6023
Ahmed Saad ID.6060
Heba Elwazzan ID.6521
Youssef Nawar ID.6602
"""

NUM_COLUMNS = 7
dictionary = dict()

# 0 | 1 | 2 | 3 | 4 | 5 | 6
ACTION_BY_PRIORITY = [3, 2, 4, 1, 5, 0, 6]


def rotation_layout(node):
    F = TextFace(node.name, tight_text=True)
    F.rotation = -90
    add_face_to_node(F, node, column=0, position="branch-right")


class Node:

    def __init__(self, parent):
        self.value = 0
        self.children = []
        self.parent = parent
        if self.parent:
            self.maximizing = not self.parent.maximizing
            self.depth = parent.depth + 1
        else:
            self.maximizing = True
            self.depth = 0

    def insertChild(self, node):
        self.children.append(node)

    # def propagateUp(self):  # function that is called when leaf node is chosen as the final decision
    #     self.parent.value = self.value
    #     self.parent.propagateUp()

    def addChild(self):
        child = Node(self)
        self.children.append(child)
        return child


def printTree(root):
    if root:
        if root.children:
            if root.maximizing:
                string = "/MAX"
            else:
                string = "/MIN"
        else:
            string = ""
        spaces = "  " * root.depth * 5
        if root.parent is None:
            parentDepth = 0
        else:
            parentDepth = root.parent.depth
        dashes = "--" * (root.depth - parentDepth) * 5
        # spaces = "  " * parentDepth * 5
        # print(f"{spaces}|{dashes}[{root.value}]{string}")
        spaces = "  " * 5
        # if root.depth != 0:
        for i in range (root.depth):
            print(f"|{spaces}", end="")
        # if root.parent and root.parent.children[len(root.parent.children) - 1].value == root.value:
        #     print(f"{dashes}-", end="")
        # else:
        #     print(f"|{spaces}", end="")

        print(f"|{dashes}[{root.value}]{string}")

        for child in root.children:
            printTree(child)


def actions(state: GameState):
    """
    Returns set of all possible actions available on the board.
    An action is valid if the top row of its column is vacant
    substitute for GameState.expand. Can be moved in GameState later
    """
    actions_list = []
    for i in ACTION_BY_PRIORITY:
        if state.isValidMove(i):
            actions_list.append(i)
    return actions_list


def terminal_state(state: GameState, k):
    """
    helper function to shorten conditions in minimax functions
    """
    if k == 0 or state.isTerminal():
        return True
    else:
        return False


# Regular minimax algorithms
# AI player will call this function
# instead of a child, the function returns an action which is a number in range(0:7)
# This makes it easier for GUI to make move
def maximizeMinimax(state: GameState, k, root: Tree):
    # Steps:
    # 1. Check if this is a terminal state, and if so return its evaluation
    #    A terminal state constitutes either the k depth = 0 was reached or the game is over (board is complete)
    if terminal_state(state, k):
        if dictionary.get(state.grid):
            return None, dictionary.get(state.grid)
        temp = state.eval()
        dictionary[state.grid] = temp
        root.name = temp
        return None, temp

    # 2. If not, set (maxChild, maxUtility) = (null, -inf)
    maxChild, maxUtility = (None, -math.inf)

    # 3. Then loop over all the state children, which are derived from all possible moves
    #    and set utility to minimize(child, k-1)
    for action in actions(state):
        _, utility = minimizeMinimax(state.makeMove(action), k - 1, root.add_child())
        # 4. Then choose maximum out of all children and return it
        if utility > maxUtility:
            maxChild, maxUtility = action, utility
            root.name = maxUtility

    return maxChild, maxUtility


def minimizeMinimax(state: GameState, k, root: Tree):
    # Steps
    # 1. Check if terminal, and if so return evaluation
    if terminal_state(state, k):
        if dictionary.get(state.grid):
            return None, dictionary.get(state.grid)
        temp = state.eval()
        dictionary[state.grid] = temp
        root.name = temp
        return None, temp

    # 2. Else set (minChild, minUtility) = (null, inf)
    minChild, minUtility = (None, math.inf)

    # 3. Then loop over each state's children and set utility to maximize(child, k-1)
    for action in actions(state):

        _, utility = maximizeMinimax(state.makeMove(action), k - 1, root.add_child())

        # 4. Choose minimum utility out of all children and return it along with the minChild
        if utility < minUtility:
            minChild, minUtility = action, utility
            root.name = minUtility

    return minChild, minUtility


def decisionMinimax(state: GameState, k):  # returns an integer between 0:7
    # The AI player is the calls maximize(state, k) and set child to it, then return it
    root = Tree()
    action, _ = maximizeMinimax(state, k, root)
    # printTree(root)
    ts = TreeStyle()
    ts.show_leaf_name = False
    ts.layout_fn = rotation_layout
    ts.rotation = 90
    ts.branch_vertical_margin = 20
    root.show(tree_style=ts)
    return action


# Minimax with alpha-beta pruning algorithms
def maximizeAlphaBeta(state: GameState, alpha, beta, k, root):
    # just like normal maximize, but when looping over children, alpha is set to max
    # and checks if alpha >= beta, breaks if true
    # updates alpha

    if terminal_state(state, k):
        if dictionary.get(state.grid):
            return None, dictionary.get(state.grid)
        temp = state.eval()
        dictionary[state.grid] = temp
        root.value = temp
        return None, temp

    maxChild, maxUtility = (None, -math.inf)

    for action in actions(state):
        _, utility = minimizeAlphaBeta(state.makeMove(action), alpha, beta, k - 1, root.addChild())

        if utility > maxUtility:
            maxChild, maxUtility = action, utility
            root.value = maxUtility

        # check if the value of beta is lower than alpha then prune the rest of the tree
        if maxUtility >= beta:
            break

        # update value of alpha
        if maxUtility > alpha:
            alpha = maxUtility

    return maxChild, maxUtility


def minimizeAlphaBeta(state: GameState, alpha, beta, k, root):
    # just like normal minimize, but when looping over children, beta is set to min
    # and checks if beta <= alpha, breaks if true
    # updates min
    if terminal_state(state, k):
        if dictionary.get(state.grid):
            return None, dictionary.get(state.grid)
        temp = state.eval()
        dictionary[state.grid] = temp
        root.value = temp
        return None, temp
    minChild, minUtility = (None, +math.inf)

    for action in actions(state):
        _, utility = maximizeAlphaBeta(state.makeMove(action), alpha, beta, k - 1, root.addChild())

        if utility < minUtility:
            minChild, minUtility = action, utility
            root.value = minUtility

        # check if the value of beta is lower than alpha then prune the rest of the tree
        if minUtility <= alpha:
            break

        # update the value of beta
        if minUtility < beta:
            beta = minUtility

    return minChild, minUtility


def decisionAlphaBeta(state: GameState, alpha, beta, k):
    # calls maximize(state, -inf, inf, k)
    # returns child returned from maximize
    root = Node(None)
    action, _ = maximizeAlphaBeta(state, alpha, beta, k, root)
    printTree(root)
    return action


def resetDict():
    global dictionary
    dictionary = dict()


# temp function to test ai in GUI
def dumbDecision(state: GameState, k):
    sleep(0.5)
    return random.randint(0, NUM_COLUMNS - 1)
