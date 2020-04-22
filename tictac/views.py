from django.shortcuts import render
from django.http import HttpResponse
from .forms import ButtonForm

EMPTY=''
NEW_GRID = [
    [EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY]
]

class TicTacToe():

    EMPTY='-'
    def __init__(self):
        self.grid=[
                [TicTacToe.EMPTY,TicTacToe.EMPTY,TicTacToe.EMPTY],
                [TicTacToe.EMPTY, TicTacToe.EMPTY, TicTacToe.EMPTY],
                [TicTacToe.EMPTY, TicTacToe.EMPTY, TicTacToe.EMPTY]
                   ]

    def is_winner(self,player):
        winner={'X':['X','X','X'],'O':['O','O','O']}

        # check for 3 possible row winners
        for i in range(3):
            if self.grid[i] == winner[player]:
                return True

        # check for 3 possible column winners
        for j in range(3):
            if [self.grid[i][j] for i in range(3)] == winner[player]: # This list comp transposes cols to rows
                return True

        # check for diagonal winners
        print('diag1=: ', )
        if [self.grid[i][i] for i in range(3)] == winner[player]: # This list comp transposes diag1 to row
                return True
        if [self.grid[i][2-i] for i in range(3)] == winner[player]: # This list comp transposes diag2 to row
                return True

        return False

    def printit(self):
        for i in range(3):
            for j in range(3):
                print(self.grid[i][j],end='')
            print()

    def move(self, player,row,col):
        existing_entry=self.grid[row-1][col-1]
        if existing_entry == TicTacToe.EMPTY:
            self.grid[row-1][col-1] = player
            return True
        if existing_entry == player:
            print("\n*****Error: you already moved to this location.  Try again.\n")
        else:
            print("\n*****Error: your opponent already claimed this move.  Try again.\n")
        return False

    def chooseplayer(self):
        while True:
            yield 'X'
            yield 'O'

    def get_next_move(self,player):
        print('Player {} it is your move.'.format(player))
        row, col = map(int, input('Enter move as "row,col", where row and col are each 1,2 or 3: ').split(','))
        if row>0 and row<=3 and col>0 and col<=3:
            return row,col
        print('Invalid row,col choice')
        return 0,0


def index(request):
    context={}
    #print("in index")
    return render(request, 'tictac/index.html', context)
    #return HttpResponse("Hello, world.")

def update_grid(grid,position,player):
    # position is 1-9
    row=int((position-1)/3)
    col=(position-1)%3
    #print("in update_grid: row,col= ",row, col)
    grid[row][col]=player
    return grid

def is_move_valid(grid,position,player):
    row=int((position-1)/3)
    col=(position-1)%3
    existing_entry = grid[row][col]
    if existing_entry == EMPTY:
        grid[row][col] = player
        return True
    """if existing_entry == player:
        #print("\n*****Error: you already moved to this location.  Try again.\n")
    else:
        #print("\n*****Error: your opponent already claimed this move.  Try again.\n")
        """
    return False

def is_winner(grid,player):
    winner={'X':['X','X','X'],'O':['O','O','O']}

    # check for 3 possible row winners
    for i in range(3):
        if grid[i] == winner[player]:
            return True

    # check for 3 possible column winners
    for j in range(3):
        if [grid[i][j] for i in range(3)] == winner[player]: # This list comp transposes cols to rows
            return True

    # check for diagonal winners
    if [grid[i][i] for i in range(3)] == winner[player]: # This list comp transposes diag1 to row
            return True
    if [grid[i][2-i] for i in range(3)] == winner[player]: # This list comp transposes diag2 to row
            return True

    return False

def grid_full(grid):
    return not EMPTY in grid[0]+grid[1]+grid[2]

def gridclick(request):

    #print (request.method)
    #button_form=ButtonForm(request.GET)

    if request.method == 'GET':
        #print("in GET section")
        #print (request.GET)
        if 'b0' in request.GET:
            clicked = 1
        elif 'b1' in request.GET:
            clicked = 2
        elif 'b2' in request.GET:
            clicked = 3
        elif 'b3' in request.GET:
            clicked = 4
        elif 'b4' in request.GET:
            clicked = 5
        elif 'b5' in request.GET:
            clicked = 6
        elif 'b6' in request.GET:
            clicked = 7
        elif 'b7' in request.GET:
            clicked = 8
        elif 'b8' in request.GET:
            clicked = 9
        else:
            clicked = 0
            request.session['clicked']=None
            request.session['grid']=NEW_GRID
            request.session['player']='X'
            grid=NEW_GRID
            request.session['game_over']=False
            request.session['status_message'] = ''
        if clicked and not request.session['game_over']:
            #print("button {} pressed".format(clicked))
            #print("grid before update=",request.session['grid'])
            request.session['clicked']=clicked
            player=request.session['player']

            # See if move is valid
            if is_move_valid(request.session['grid'],clicked, player) and not request.session['game_over']:
                # modify our grid to reflect button clicked
                new_grid=update_grid(request.session['grid'],clicked, player)
                #print(new_grid)
                request.session['grid']=new_grid
                grid=new_grid

                # Check if any player has won
                if is_winner(grid, player):
                    #print("Player {} has won!".format(player))
                    request.session['status_message']='Player {} has won!'.format(player)
                    request.session['game_over']=True
                elif grid_full(grid):
                    #print("Grid is full, but no winner")
                    request.session['status_message'] = 'Grid is full, but no winner'
                    request.session['game_over'] = True

                else:
                    # Toggle player
                    if request.session['player'] == 'X':
                        request.session['player'] = 'O'
                        player = 'O'
                    else:
                        request.session['player'] = 'X'
                        player = 'X'
                    request.session['status_message'] = 'Player {}, please make your move.'.format(player)
            else:
                # An invalid move was made, so no change to grid
                grid=request.session['grid']

            # prepare context so that new grid is rendered
        context={'grid': request.session['grid'], 'message': request.session['status_message']}
        #print("context=: ", context)
    return render(request, 'tictac/tictactoe.html', context)
