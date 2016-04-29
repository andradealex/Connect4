# Connect 4!

import random
import time
from copy import copy


def print_board(board):

    '''Prints the board, along with the number of each column above.
    Returns None.
    '''

    out = [''.join('  {} '.format(n+1) for n in range(BOARDSIZE))]
    out.append('+ - '*BOARDSIZE + '+')
    for y in range(BOARDSIZE, 0, -1):
        next_row = '| '
        for x in range(1, BOARDSIZE+1):
            next_row += board.get((x,y), ' ') + ' | '
        out.append(next_row)
        out.append('+ - '*BOARDSIZE + '+')
    print('\n' + '\n'.join(out) + '\n')           


def get_player_move():

    move = input("Choose a column to place your piece into. ")
    while True:
        try:
            move = int(move)
        except ValueError:
            move = input("That's not a valid move. ")
            continue
        if not 0 < move <= BOARDSIZE:
            move = input("That's not a valid move. ")
            continue
        while (move, 0) in board:
            move = input("There's no more room in that column. ")
            continue
        return move


def get_cpu_move():

    '''Chooses a column for any cpu player to place their piece into.
    Returns an int.

    Currently uses a simple random choice.
    '''

    # Check if there's a winning move this turn.
    
    for move in range(1, BOARDSIZE+1):
        if try_moves([move]):
            return move

    # Otherwise choose a random column.

    moves = [x+1 for x in range(BOARDSIZE)]
    move = random.choice(moves)
    while (move, 0) in board:
        move = random.choice(moves)
    return move


    '''
    could try to do a search n moves deep for each possible move.
    build a dict mapping from possible columns to chance of winning.
    for every position n or fewer moves away that results in a win, for
    the cpu, add one/depth, and if the player wins, minus one/depth.
    random choice from the highest scoring moves. (this formula will
    overestimate probabilities as it doesn't take into account the possible
    moves that the player can make in between).
    O(n**2), so will benefit from the more efficient game_won() a lot.
    can increase n for higher difficulty, although this should ideally scale
    BOARDSIZE, because this will also increase search space due to an increased
    number of possible moves.
    I think a depth-first search would make for easier pruning of routes once
    they reach a win scenario.

    How to do the search:
    Probably need a function that checks a sequence of moves to see if it wins.
    Need to make sure this function doesn't alter the main board list.
    I then only need to store a list of max size BOARDSIZE. Keep this list
    separate from the poss_moves dict. Extend the list
    move by move, and change the relevant poss_moves dict value whenever you
    reach a win state, and stop searching that branch. After a level has
    been exhausted, either by all possible moves reaching a win, or (more
    likely) by reaching the max search depth, you can move back one level.
    Not sure if I can prune branches as I go, or if I'll have to keep a
    pruning table separately.
    '''


def drop_piece(board, move):

    '''Accepts a dict, board, to which move will be applied, and
    an int, move, and updates the board by placing the player's
    piece in the lowest free spot in that number column.
    Returns the y co-ordinate it is placed at, as an int.

    This will probably need updating in tandem with try_moves(), or maybe
    just use different functions for trying moves, and putting this code in
    the main game loop.
    '''

    for y in range(1, BOARDSIZE+1):
        if (move, y) not in board:
            board[(move, y)] = player
            return y            
        

def game_won(board, x, y):

    '''Accepts two ints, x and y, which are the x and y co-ordinates of the
    last move made. Checks to see if there is a winning line of length WINLEN
    on the board by checking every line that includes the last placed piece.
    Returns bool.
    '''

    checkrange = range(1-WINLEN, WINLEN)
    horizontal = ''
    vertical = ''
    forwardslash = ''
    backslash = ''
    for n in checkrange:
        horizontal += board.get((x-n,y), ' ')
        vertical += board.get((x,y-n), ' ')
        forwardslash += board.get((x+n,y+n), ' ')
        backslash += board.get((x+n,y-n), ' ')
    lines = [horizontal, vertical, forwardslash, backslash]

    win = board[(x,y)]*WINLEN
    for line in lines:
        if win in line:
            return True
    return False


def try_moves(moves):

    '''Accepts a list of ints, moves, and applies them in order to see
    if they result in a win. Returns a bool.

    Ideally this can be changed to to only call game_won() after all moves
    have been applied, however it depends how get_cpu_move() ends up being
    implemented.

    Apparently I need to use a chainmap for this (for optimum speed, and
    therefore to maximise the possible search depth. Now to figure out how
    to use chainmaps...
    '''

    temp_board = copy(board)

    for m in moves:
        last_y = drop_piece(temp_board, m)
        if game_won(temp_board, m, last_y):
            return True
    return False


def testboard():

    for x in range(1, 5):
        board[(x,7-x)] = 'X'
    

        
# Settings

BOARDSIZE = 8
WINLEN = 4
players = ('X', 'O')
YOU = players[0]
test = False


# Start

board = {}
turn = random.choice([n for n in range(len(players))])

if test:
    testboard()

print_board(board)

# Game Loop

while True:

    player = players[turn % len(players)]

    print("\nIt is {}'s turn.".format(player))

    if player != YOU:
        move = get_cpu_move()
        time.sleep(0) # Suspense/Annoyance control
    else:
        move = get_player_move()
    
    last_y = drop_piece(board, move)

    print_board(board)

    if game_won(board, move, last_y):
        print("{} has won!".format(player))
        break

    if len(board) == BOARDSIZE**2:
        print("No one wins.")
        break

    turn += 1

    
