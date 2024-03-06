import copy
import numpy as np


class BoardState:
    """
    BoardState represents a single Tic-Tac-Toe board in a given state.
    1 is -> x       -1 is -> o      0 -> Empty Cell
    x|o|x
    o|x|o   =   [[1,-1,1],[-1,1,-1],[1,0,0]]
    x| |
    """
    def __init__(self, depth=0, board=[[0, 0, 0], [0, 0, 0], [0, 0, 0]]):
        self.board = board
        self.cols = len(board)
        self.rows = len(board[0])
        self.depth = depth
        # TODO: generate magic numbers based on board size
        self.magicValues = [[8, 1, 6], [3, 5, 7], [4, 9, 2]]  # Uses Magic Squares to check goal-state
        self.tile_worth = [[2, 1, 2], [2, 5, 2], [2, 1, 2]]  # Associated 'worth' of each tile for heuristics
        self.h_value = self.find_h()

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

    # Heuristic function to estimate distance of board to goal-state
    def find_h(self):
        goal_state = self.is_goal_state()
        if goal_state == 1 or goal_state == -1:
            return 1000*goal_state

        full_item_list = []  # list of every direction's elements
        score = 0

        # Fill 'full_item_list' with lists of all rows, columns, and diagonals.
        np_array = np.array(self.board) # Using numpy to get diagonals from self.board 2d array
        primary_diagonals = [np_array[::-1,:].diagonal(i) for i in range(-self.rows+1, self.cols)]
        secondary_diagonals = [np.flip(np_array[::-1,:], 1).diagonal(i) for i in range(-self.rows+1, self.cols)]
        for column_index in range(self.cols):
            full_item_list.append(np_array[:,column_index])
        for row_index in range(self.rows):
            full_item_list.append(np_array[row_index,:])
        full_item_list.extend(primary_diagonals)
        full_item_list.extend(secondary_diagonals)

        # Calculate score from rows, columns, and diagonals contained within full_item_list
        for sub_array in full_item_list:
            if len(sub_array) > 1:
                for element in range(len(sub_array)-1):
                    if sub_array[element] == sub_array[element+1]:
                        score += (sub_array[element]*10)

        # Give score to heuristic based on how 'desirable' a tile is according to self.tile_worth
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != 0:
                    score += self.tile_worth[row][col]

        return score

    # Generate all mutations of self and return as a list
    def get_children(self, player=1):
        x = 0
        y = 0
        new_boards = []  # fill with all possible child boards
        while x < self.rows:
            while y < self.cols:
                if self.board[x][y] == 0:
                    # create child board, modify it with new player action. (ex: new board with x at [0,1])
                    new_child = copy.deepcopy(self.board)
                    new_child[x][y] = player
                    new_boards.append(BoardState(board=new_child, depth=self.depth+1))
                y += 1
            y = 0
            x += 1
        return new_boards

    # Returns True if this board is a goal, meaning either 3 x's or 3 o's in a row.
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

# Search for any board solution
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

# Depth-limited Minimax Algorithm - Simulates two player interaction
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
    # board = BoardState()
    # print("current board")
    # board.print_board()
    # print("goalState")
    # print(board.is_goal_state())
    # children = (board.get_children(1))
    # print("child boards")
    # for board in children:
    #     print(board)
    #
    # print("board_two")
    # board_two = BoardState(board=[[0, -1, -1], [1, 1, 1], [1, 1, 1]])
    # children_two = board_two.get_children()
    # print("child_two boards")
    # for board in children_two:
    #     print(board)
    #
    # print("A* Search")
    # print(a_star())
    #
    # print()
    # print("A* Search no solution")
    # print(a_star(start=[[0, 1, -1],[1, -1, 1],[-1, 1, -1]]))
    #
    # print("hueristic")
    # board_three = BoardState(board=[[0, 1, -1], [1, 0, 1], [1, 0, 1]])
    # print(board_three.find_h())
    # min_max_result = min_max(BoardState(board=[[0, 0, 0], [0, 0, 0], [0, 0, 0]]), 1000, True  , 0)
    # print("min_max")
    # print(min_max_result)

    min_max_result = min_max(BoardState(board=[[1, 0, 0], [0, -1, 0], [0, 0, 0]]), 1000, True, 0)
    print("min_max 2nd test")
    print(min_max_result)
    #print(min_max_result.h_value)
