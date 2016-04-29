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

    '''Asks the player for their move. Checks that the move is valid,
    and then returns it as an int.
    '''

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
        if (move, 8) in board:
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
        if (move, 8) not in board:
            if try_moves([move]):
                return move

    # Otherwise choose a random column.

    print()
    print('CPU move selections:')
    moves = [x+1 for x in range(BOARDSIZE)]
    move = random.choice(moves)
    print(move)
    while (move, 8) in board:
        move = random.choice(moves)
    print()
    return move


def drop_piece(board, move):

    '''Accepts a dict, board, to which move will be applied, and
    an int, move, and updates the board by placing the player's
    piece in the lowest free spot in that number column.
    Returns the y co-ordinate it is placed at, as an int.
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
    '''

    temp_board = copy(board)

    for m in moves:
        last_y = drop_piece(temp_board, m)
        if game_won(temp_board, m, last_y):
            return True
    return False


def testboard():

    '''Used to set a non-blank starting position for the board to
    to test.
    '''
    
    pass
    

        
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

    print('X: {}   Y: {}'.format(move, last_y))

    if game_won(board, move, last_y):
        print("{} has won!".format(player))
        break

    if len(board) == BOARDSIZE**2:
        print("No one wins.")
        break

    turn += 1
