import math
import random

from code.classes.board import Board


class Game():
    """
    Creates game object to play Rush Hour. Checks for possible moves,
    picks random move and checks for win.
    """
    def __init__(self, source_file):
        self.board = Board(source_file)
        self.moves = []


    def find_moves(self):
        """
        Creates list of possible moves.
        """

        # create new move list
        valid_moves = []

        # loop over cars on board
        for car in self.board.cars:
            row = car.row
            col = car.col

            # check for empty spaces left and right from horizontal car
            if car.orientation == 'H':
                if self.board.layout[row][col - 1] == '_' and col != 0:
                    valid_moves.append([car, -1])

                # prevent border error with try/except
                try:
                    if self.board.layout[row][col + car.length] == '_':
                        valid_moves.append([car, 1])
                except IndexError:
                    pass

            # check for empty spaces up and down from vertical car
            if car.orientation == 'V':
                if self.board.layout[row - 1][col] == '_' and row != 0:
                    valid_moves.append([car, -1])

                # prevent border error
                try:
                    if self.board.layout[row + car.length][col] == '_':
                        valid_moves.append([car, 1])
                except IndexError:
                    pass

        return valid_moves

    def move(self, choice):

        car = choice[0]
        direction = choice[1]

        # set new coordinates for moved car
        if car.orientation == 'H':
            car.col += direction
        elif car.orientation == 'V':
            car.row += direction

        # add move to list of moves (if latest move is same, just add 1 to move)
        if self.moves and [car.name, direction] == self.moves[-1]:
            self.moves[-1][1] += direction
        else:
            self.moves.append([car.name, direction])

    def win(self):
        """
        Returns true and prints success if red car (XX) is at exit.
        Example: 6x6 exit is at (3, 6) --> index [2][5].
        """

        # get column right of red car
        col_x = [car.col + 2 for car in self.board.cars if car.name == 'X'][0]

        # get coordinates of exit
        row_e = math.ceil(self.board.size / 2) - 1
        col_e = self.board.size - 1

        # check if X is on exit or the row towards exit is empty
        if self.board.layout[row_e][col_e] == 'X' or all(self.board.layout[row_e][col_x:] == '_'):

            # add last moves of X to moves list
            moves_left = self.board.size - col_x
            self.moves.append(['X', moves_left])

            # print("success")
            return True

        return False
