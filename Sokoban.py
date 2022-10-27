"""
Name: Aaron Heald
UPI: ahea795
Description: Simulates a game of Sokoban
"""


class Sokoban:
    def __init__(self, board):
        self.__board = board
        self.__steps = 0
        self.__board_state = []
        self.__width = len(board[:][1])
        self.__height = len(board[:][:])
        self.__box_amount = 0
        self.__hole_amount = 0
        self.__hole_indexes = []

    def find_player(self):
        y = -1
        for row in self.__board:
            y += 1
            x = -1
            for column in row:
                x += 1
                if column.lower() == "p":
                    return y, x
        return 0, 0

    def complete(self):
        for row in self.__board:
            if "o" in row:
                return False
        return True

    def hole_filler(self, direction, movement):
        holes = self.__hole_indexes
        if holes != []:
            x, y = self.__hole_indexes[0]
            if direction == "a" or direction == "d":
                if movement < 0:
                    x += movement
                    y -= 1
                else:
                    x -= movement
                self.__board[y][x] = " "
            else:
                if movement < 0:
                    y += movement
                else:
                    y -= movement
                self.__board[y][x] = " "
            self.__hole_indexes.pop()
            self.__box_amount -= 1

    def get_steps(self):
        return self.__steps

    def get_number_of_boxes(self):
        box_count = 0
        for row in self.__board:
            if "#" in row:
                for column in row:
                    if "#" in column:
                        box_count += 1
        if box_count < self.__box_amount:
            return box_count
        else:
            self.__box_amount = box_count
            return box_count

    def get_number_of_holes(self):
        hole_count = 0
        for row in self.__board:
            if "o" in row:
                for column in row:
                    if "o" in column:
                        hole_count += 1
        if hole_count < self.__hole_amount:
            return hole_count
        else:
            self.__hole_amount = hole_count
            return hole_count

    def restart(self):
        for moves in range(self.__steps):
            self.undo()

    def undo(self, box_collision=False):
        if self.__steps > 0:
            if box_collision:
                self.__board = self.__board_state[-1]
            else:
                self.__board_state.pop()
                self.__board = self.__board_state[-1]
                self.__steps -= 1

    def hole_adding(self, x, y, new_x, new_y):
        if x < new_x:
            x = new_x + 1
        else:
            y = new_y + 1
        self.__hole_indexes.append((x, y))

    def movement_direction(self, direction):
        if direction == "w" or direction == "a":
            return -1
        else:
            return 1

    def illegal_move_check(self, direction, movement, player=(0, 0)):
        x, y = player
        if direction == "a" or direction == "d":
            position_check = self.__board[y % self.__height][(x+movement) % self.__width]
            if position_check == "*":
                return False
        else:
            position_check = self.__board[(y+movement) % self.__height][x % self.__width]
            if position_check == "*":
                return False
        return True

    def box_move_action(self, x, y, movement, direction):
        new_x, new_y = x, y
        if direction == "a" or direction == "d":
            new_x = (x + movement) % self.__width
            if (new_x, y) not in self.__hole_indexes:
                self.__board[y % self.__height][x % self.__width] = " "
                self.__board[y % self.__height][new_x] = "#"
            else:
                self.undo()
        else:
            new_y = (y + movement) % self.__height
            if (x, new_y) not in self.__hole_indexes:
                self.__board[y % self.__height][x % self.__width] = " "
                self.__board[new_y][x % self.__width] = "#"
            else:
                self.undo(True)
        return new_x, new_y

    def box_move(self, movement, direction, player=(0, 0)):
        x, y = player
        legal_move = self.illegal_move_check(direction, movement, (x, y))
        self.get_number_of_holes()
        position_check = self.__board[y % self.__height][x % self.__width]
        if legal_move:
            if position_check == "#":
                new_x, new_y = self.box_move_action(x, y, movement, direction)
                final_hole_amount = self.get_number_of_holes()
                if final_hole_amount < self.__hole_amount:
                    self.hole_adding(x, y, new_x, new_y)
                    self.__hole_amount -= 1
        return legal_move

    def move_action(self, box_moved, x, y, player_origin=(0, 0)):
        original_y, original_x = player_origin
        board_check = self.__board[y % self.__height][x % self.__width]
        if board_check != "o":
            if not box_moved and board_check == "#":
                self.__board[original_y % self.__height][original_x % self.__width] = "P"
            else:
                self.__board[y % self.__height][x % self.__width] = "P"
                self.__steps += 1
            final_box_amount = self.get_number_of_boxes()
            if final_box_amount < self.__box_amount:
                box_collision = True
                self.undo(box_collision)
            return True
        else:
            self.__board[original_y % self.__height][original_x % self.__width] = "P"
        return False

    def move(self, direction):
        if self.__steps == 0:
            self.board_state_copying()
        player_origin = y, x = self.find_player()
        movement = self.movement_direction(direction)
        legal_move = self.illegal_move_check(direction, movement, (x, y))
        if legal_move:
            self.__board[y % self.__height][x % self.__width] = " "
            if direction == "a" or direction == "d":
                x += movement
            else:
                y += movement
            box_moved = self.box_move(movement, direction, (x, y))
            moved_player = self.move_action(box_moved, x, y, player_origin)
            self.hole_filler(direction, movement)
            if moved_player:
                self.board_state_copying()

    def board_state_copying(self):
        board_list = self.__board
        board_state = list(list(board_row) for board_row in board_list)
        self.__board_state.append(board_state)

    def __str__(self):
        sokoban_board = ""
        for row in self.__board:
            for column in row:
                sokoban_board += column + " "
            sokoban_board = sokoban_board[:-1] + "\n"

        return sokoban_board[:-1]


def main(board):
    game = Sokoban(board)
    message = 'Press w/a/s/d to move, r to restart, or u to undo'
    print(message)
    while not game.complete():
        print(game)
        move = input('Move: ').lower()
        while move not in ('w', 'a', 's', 'd', 'r', 'u'):
            print('Invalid move.', message)
            move = input('Move: ').lower()
        if move == 'r':
            game.restart()
        elif move == 'u':
            game.undo()
        else:
            game.move(move)
    print(game)
    print(f'Game won in {game.get_steps()} steps!')


# This is here for you to test your code. You will need to test your code
# yourself for this assignment. Remove any testing code (including the code
# provided below) when you submit this file.
#
# The only code in your submission should be:
#   - the Sokoban class
#   - the main function
#
# There should be no other code included in your submission.
test_board = [
    ['*', '*', '*', '*', '*', '*', '*', '*'],
    ['*', ' ', ' ', ' ', ' ', ' ', ' ', '*'],
    ['*', 'P', ' ', '#', ' ', ' ', ' ', '*'],
    ['*', '*', '*', '*', '*', ' ', '#', '*'],
    ['*', 'o', ' ', ' ', ' ', ' ', ' ', '*'],
    ['*', ' ', ' ', ' ', ' ', ' ', 'o', '*'],
    ['*', '*', '*', '*', '*', '*', '*', '*']
]
main(test_board)
