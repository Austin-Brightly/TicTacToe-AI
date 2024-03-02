# This is a sample Python script.
import copy
import numpy as np

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
class BoardState:
    def __init__(self, depth=0, board=[[0,0,0],[0,0,0],[0,0,0]]):
        self.board = board
        self.cols = len(board)
        self.rows = len(board[0])
        self.depth = depth
        self.magicValues = [[8, 1, 6], [3, 5, 7], [4, 9, 2]]
        self.h_value = self.find_h()
        #board contains the state of a tic-tac-toe board
        # -1 is -> x       1 is -> o
        #self.board = [[0] * cols] * rows <- bugged

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

    # def find_hueristic(self):
    #     arr = []
    #     arr_two = []
    #     count = 0
    #     count_two = 0
    #     for x in self.board:
    #         for y in x:
    #             if y==1:
    #                 arr.append(self.magicValues[count][count_two])
    #             elif y==-1:
    #                 arr_two.append(self.magicValues[count][count_two])
    #             count_two+=1
    #         count+=1
    #         count_two=0
    #
    #     arr.sort()
    #     arr_two.sort()
    #     arr_score = 0
    #     for i in range(len(arr)):
    #         a = arr[i]
    #         start = i+1
    #         end = len(arr)-1
    #         while(start < end):
    #             b = arr[start]
    #             c = arr[end]
    #             if(a + b + c == 15):
    #                 arr_score += 100
    #     return 0

    def find_h(self, patternlength=2):
        goal_state = self.goalState()
        if(goal_state == 1 or goal_state == -1):
            return 1000*goal_state

        full_item_list = []

        score = 0

        #primary_diagnals = [self.board[i][i] for i in range(len(self.board))]
        #secondary_diagnals = [self.board[i][len(self.board)-i-1] for i in range(len(self.board))]
        np_array = np.array(self.board)
        primary_diagnals = [np_array[::-1,:].diagonal(i) for i in range(-self.rows+1, self.cols)]
        secondary_diagnals = [np.flip(np_array[::-1,:], 1).diagonal(i) for i in range(-self.rows+1, self.cols)]


        #print("primary and secondary diags")
        #print(primary_diagnals)
        #print(secondary_diagnals)

        for column_index in range(self.cols):
            full_item_list.append(np_array[:,column_index])
        for row_index in range(self.rows):
            full_item_list.append(np_array[row_index,:])
        full_item_list.extend(primary_diagnals)
        full_item_list.extend(secondary_diagnals)


        for sub_array in full_item_list:
            if(len(sub_array)>1):
                for element in range(len(sub_array)-1):
                    if(sub_array[element] == sub_array[element+1]):
                        score += (sub_array[element]*10)

        #print("actual board:")
        #print(self.board)
        return score


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
        print("current player: ", current_player)
        print(currentItem)
        print()
        closed.append(currentItem)
        currentChildren = currentItem.getChildren(player=current_player)
        for item in currentChildren:
            open.append(item)
            #If goal board found, return success == 1
            if(item.goalState() == True):
                return [item, True]
        # change turn
        current_player = (current_player * -1)
    # no solution, return success==0
    return [closed, False]





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

    print()
    print("A* Search no solution")
    print(a_star(start=[[0,1,-1],[1,-1,1],[-1,1,-1]]))

    print("hueristic")
    #board_three = BoardState(board=[[0, -1, -1],[1, 0, 1],[1, 0, 1]])
    board_three = BoardState(board=[[0, 1, -1], [1, 0, 1], [1, 0, 1]])
    print(board_three.find_h())