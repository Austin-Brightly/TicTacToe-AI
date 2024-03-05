import copy
import numpy as np


class BoardState:
    def __init__(self, depth=0, board=[[0, 0, 0], [0, 0, 0], [0, 0, 0]]):
        self.board = board
        self.cols = len(board)
        self.rows = len(board[0])
        self.depth = depth
        self.magicValues = [[8, 1, 6], [3, 5, 7], [4, 9, 2]]
        self.tile_worth = [[2, 1, 2], [2, 5, 2], [2, 1, 2]]
        self.h_value = self.find_h()
        # board contains the state of a tic-tac-toe board
        # -1 is -> x       1 is -> o
        # self.board = [[0] * cols] * rows <- bugged

    def __repr__(self):
        return_str = ""
        for item in self.board:
            return_str+=str(item)
            return_str+="\n"
        return return_str

    def print_board(self):
        for row in self.board:
            print(row)
        print()
        for row in self.magicValues:
            print(row)

    def find_h(self):
        goal_state = self.is_goal_state()
        if goal_state == 1 or goal_state == -1:
            return 1000*goal_state

        full_item_list = []  # list of every direction's elements
        score = 0

        np_array = np.array(self.board)
        primary_diagonals = [np_array[::-1,:].diagonal(i) for i in range(-self.rows+1, self.cols)]
        secondary_diagonals = [np.flip(np_array[::-1,:], 1).diagonal(i) for i in range(-self.rows+1, self.cols)]

        for column_index in range(self.cols):
            full_item_list.append(np_array[:,column_index])
        for row_index in range(self.rows):
            full_item_list.append(np_array[row_index,:])
        full_item_list.extend(primary_diagonals)
        full_item_list.extend(secondary_diagonals)

        for sub_array in full_item_list:
            if len(sub_array) > 1:
                for element in range(len(sub_array)-1):
                    if sub_array[element] == sub_array[element+1]:
                        score += (sub_array[element]*10)

        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != 0:
                    score += self.tile_worth[row][col]

        return score

    def get_children(self, player=1):
        x = 0
        y = 0
        new_boards = []
        while x < self.rows:
            while y < self.cols:
                if self.board[x][y] == 0:
                    temp = copy.deepcopy(self.board)
                    temp[x][y] = player
                    new_depth = self.depth+1
                    new_boards.append(BoardState(board=copy.deepcopy(temp[:]), depth=new_depth))
                y += 1
            y = 0
            x += 1
        return new_boards

    def is_goal_state(self):
        x = 0
        y = 0

        #check rows
        while x < self.rows:
            player_one_sum = 0
            player_two_sum = 0
            while y < self.cols:
                if self.board[x][y] == 1:
                    player_one_sum += self.magicValues[x][y]
                elif self.board[x][y] == -1:
                    player_two_sum += self.magicValues[x][y]
                y += 1
            y = 0
            if player_one_sum == 15:
                return 1
            elif player_two_sum == 15:
                return -1
            x += 1

        # check columns (can merge with previous loop)
        x = 0
        y = 0
        while x < self.rows:
            player_one_sum = 0
            player_two_sum = 0
            while y < self.cols:
                if self.board[y][x] == 1:
                    player_one_sum += self.magicValues[y][x]
                elif self.board[y][x] == -1:
                    player_two_sum += self.magicValues[y][x]
                y += 1
            y = 0
            if player_one_sum == 15:
                return 1
            elif player_two_sum == 15:
                return -1
            x += 1

        # figure out more elegant diagonal check
        # hard coded for now
        # TODO: Use numpy to get diagonals, then use magic numbers for quick calulation
        diag_one = self.board[0][0] + self.board[1][1] + self.board[2][2]
        diag_two = self.board[2][0] + self.board[1][1] + self.board[0][2]
        if diag_one == 3 or diag_two == 3:
            return 1
        elif diag_one == -3 or diag_two == -3:
            return -1

        # tie result
        return 0

#search for any solution
def a_star(start=[[0, 0, 0],[0, 0, 0],[0, 0, 0]]):
    # open is sorted by hueristic value
    open = [BoardState(board=start)]
    closed = []
    # players are [1=x,-1=o]
    current_player = 1

    # while boardstates are on open, search for goal.
    while len(open)>0:
        #open.sort(reverse=True, key=lambda x: x.h_value)
        current_item = open.pop(open.index(min(open, key=lambda x: x.h_value)))
        #current_item = open.pop(0)
        print("current player: ", current_player)
        print(current_item)
        print()

        closed.append(current_item)
        current_children = current_item.get_children(player=current_player)
        for item in current_children:
            open.insert(0, item)
            # If goal board found, return success == 1
            if item.is_goal_state():
                return [item, True, current_player*-1]
        # change turn
        current_player = (current_player * -1)
    # no solution, return success==0
    return [closed, False]


#two player interactive solution - depth limited minimax algoritm
# def min_max(board_given, depth, maximizing_player, tracking_depth):
#     if depth == 0 or board_given.is_goal_state():
#         return board_given
#     if maximizing_player:
#         value = board_given
#         for child in board_given.get_children(player=1):
#             if child.is_goal_state():
#                 minval = min_max(child, depth-1, False, tracking_depth=tracking_depth+1)
#                 value = max(value, minval, key=lambda x: x.h_value)
#                 val = value
#         return value
#     else:# (* minimizing player *)
#         value = board_given
#         for child in board_given.get_children(player=-1):
#             value = min(value, min_max(child, depth-1, True, tracking_depth=tracking_depth+1), key=lambda x: x.h_value)
#         return value
def min_max(board_given, depth, maximizing_player, tracking_depth=0):
    if board_given.is_goal_state() or depth <= 0:
        return board_given
    best_item = board_given
    if maximizing_player:
        children_list = board_given.get_children(player=1)
        #for item in children_list:
            # if compare_item is None:
            #     compare_item = board_given
        best_item = max(children_list, key=lambda x: x.h_value)
        compare_item = min_max(best_item, depth - 1, False)
    else:
        children_list = board_given.get_children(player=-1)
        #for item in children_list:
        best_item = min(children_list, key=lambda x: x.h_value)
        compare_item = min_max(best_item, depth - 1, True)
    return compare_item



if __name__ == '__main__':
    board = BoardState()
    print("current board")
    board.print_board()
    print("goalState")
    print(board.is_goal_state())
    children = (board.get_children(1))
    print("child boards")
    for board in children:
        print(board)

    print("board_two")
    board_two = BoardState(board=[[0, -1, -1], [1, 1, 1], [1, 1, 1]])
    children_two = board_two.get_children()
    print("child_two boards")
    for board in children_two:
        print(board)

    print("A* Search")
    print(a_star())

    print()
    print("A* Search no solution")
    print(a_star(start=[[0, 1, -1],[1, -1, 1],[-1, 1, -1]]))

    print("hueristic")
    board_three = BoardState(board=[[0, 1, -1], [1, 0, 1], [1, 0, 1]])
    print(board_three.find_h())
    min_max_result = min_max(BoardState(board=[[0, 0, 0], [0, 0, 0], [0, 0, 0]]), 1000, True, 0)
    print("min_max")
    print(min_max_result)

    min_max_result = min_max(BoardState(board=[[1, 0, 0], [0, -1, 0], [0, 0, 0]]), 1000, True, 0)
    print("min_max 2nd test")
    print(min_max_result)
    #print(min_max_result.h_value)
