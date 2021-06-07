# Algorithms go here


def actions():
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    pass


# Regular minimax algorithms
def maximizeMinimax(state, k):
    # Steps:
    # 1. Check if this is a terminal state, and if so return its evaluation
    #    A terminal state constitutes either the k depth = 0 was reached or the game is over (board is complete)
    # 2. If not, set (maxChild, maxUtility) = (null, -inf)
    # 3. Then loop over all the state children, which are derived from all possible moves
    #    and set utility to minimize(child, k-1)
    # 4. Then choose maximum out of all children and return it
    pass


def minimizeMinimax(state, k):
    # Steps
    # 1. Check if terminal, and if so return evaluation
    # 2. Else set (minChild, minUtility) = (null, inf)
    # 3. Then loop over each state's children and set utility to maximize(child, k-1)
    # 4. Choose minimum utility out of all children and return it along with the minChild
    pass


def decisionMinimax(state, k):
    # The AI player is the
    # call maximize(state, k) and set child to it, then return it
    pass


# Minimax with alpha-beta pruning algorithms
def maximizeAlphaBeta(state, alpha, beta, k):
    # just like normal maximize, but when looping over children, alpha is set to max
    # and checks if alpha >= beta, breaks if true
    pass


def minimizeAlphaBeta(state, alpha, beta, k):
    # just like normal minimize, but when looping over children, beta is set to min
    # and checks if beta <= alpha, breaks if true
    pass


def decisionAlphaBeta(state, k):
    # calls maximize(state, -inf, inf, k)
    # returns child returned from maximize
    pass



