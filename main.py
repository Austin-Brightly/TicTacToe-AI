# This is a sample Python script.
import copy

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
class BoardState:
    def __init__(self, cols=3, rows=3, depth=0, board=[[0,0,0],[0,0,0],[0,0,0]]):
        self.cols = cols
        self.rows = rows
        self.depth = depth
        self.h_value = 0
        #board contains the state of a tic-tac-toe board
        # -1 is -> x       1 is -> o
        #self.board = [[0] * cols] * rows <- bugged
        self.board = board
        # #arbitary size board generator (unfinished)
        # x = 0
        # y = 0
        # while(x<self.rows and y<self.cols):
        #     #self.board[x][y] = 1
        #     x+=1
        #     y+=1
        #hard code 3x3 magic number board, will add arbitary sizes later
        self.magicValues = [[8,1,6],[3,5,7],[4,9,2]]

    def __repr__(self):
        return_str = ""
        for item in self.board:
            return_str+=str(item)
            return_str+="\n"
        return return_str
    def printBoard(self):
        for row in self.board:
            print(row)
        print()
        for row in self.magicValues:
            print(row)

    def getChildren(self, player=1):
        x=0
        y=0
        new_boards = []
        while (x < self.rows):
            while (y < self.cols):
                if (self.board[x][y] == 0):
                    temp = copy.deepcopy(self.board)
                    temp[x][y] = player
                    new_depth=self.depth+1
                    new_boards.append(BoardState(board=copy.deepcopy(temp[:]), depth=new_depth))
                y+=1
            y=0
            x+=1

        return new_boards

    def goalState(self):
        x = 0
        y = 0

        #check rows
        while (x < self.rows):
            player_one_sum=0
            player_two_sum=0
            #print("row "+str(x)+": ", self.board[x])
            while(y < self.cols):
                if(self.board[x][y] == 1):
                    player_one_sum += self.magicValues[x][y]
                elif (self.board[x][y] == -1):
                    player_two_sum += self.magicValues[x][y]
                y+=1
            y=0
            #print("p1: "+str(player_one_sum))
            #print("p2: "+str(player_two_sum))
            if(player_one_sum == 15):
                return 1
            elif(player_two_sum == 15):
                return -1
            x+=1

        #check columns (can merge with previos loop)
        x=0
        y=0
        while (x < self.rows):
            player_one_sum = 0
            player_two_sum = 0
            #print("row " + str(x) + ": ", self.board[x])
            while (y < self.cols):
                if (self.board[y][x] == 1):
                    player_one_sum += self.magicValues[y][x]
                elif (self.board[y][x] == -1):
                    player_two_sum += self.magicValues[y][x]
                y += 1
            y = 0
            #print("p1: " + str(player_one_sum))
            #print("p2: " + str(player_two_sum))
            if (player_one_sum == 15):
                return 1
            elif (player_two_sum == 15):
                return -1
            x += 1

        #figure out more elegant diagonal check
        #hard coded for now
        diag_one = self.board[0][0] + self.board[1][1] + self.board[2][2]
        diag_two = self.board[2][0] + self.board[1][1] + self.board[0][2]
        if(diag_one == 3 or diag_two == 3):
            return 1
        elif(diag_one == -3 or diag_two == -3):
            return -1

        #tie result
        return 0


def best_first_search(initial_board):
    open = [initial_board]
    closed = []
    while(len(open) > 0):
        current = open[0]
        current.isGoal()

def a_star(start=[[0,0,0],[0,0,0],[0,0,0]]):
    #open is sorted by hueristic value
    open = [BoardState(board=start)]
    closed = []
    #players are [1,-1]
    current_player = 1

    while len(open)>0:
        open.sort(reverse=True, key=lambda x: x.h_value)
        currentItem = open.pop()
        closed.append(currentItem)
        currentChildren = currentItem.getChildren(player=current_player)
        for item in currentChildren:
            open.append(item)
            #If goal board found, return success == 1
            if(item.goalState() == True):
                return [item, 1]
        # change turn
        current_player = (current_player * -1)
    # no solution, return success==0
    return [closed, 0]





if __name__ == '__main__':
    board = BoardState()
    print("current board")
    board.printBoard()
    print("goalState")
    print(board.goalState())
    children = (board.getChildren(1))
    print("child boards")
    for board in children:
        print(board)

    print("board_two")
    board_two = BoardState(board=[[0,-1,-1],[1,1,1],[1,1,1]])
    children_two = board_two.getChildren()
    print("child_two boards")
    for board in children_two:
        print(board)

    print("A* Search")
    print(a_star())