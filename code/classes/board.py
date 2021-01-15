import csv
import matplotlib.pyplot as plt
import numpy as np
import re
import time

from code.classes.car import Car


class Board():
    """
    Creates board for Rush Hour game. Loads data for beginning position.
    """
    def __init__(self, source_file):

        # load cars from datafile
        self.cars = self.load_cars(source_file)

        # get board size from filename
        result = re.search('Rushhour(.*)x', source_file)
        self.size = int(result.group(1))

        # create first layout
        self.layout = self.create_layout()

    def load_cars(self, source_file):
        """
        Creates list of Car objects from data in source file.
        """

        # create empty list for Car objects
        cars_list = []

        # open source file
        with open(source_file, "r") as reader:
            datafile = csv.reader(reader)

            # skip header
            next(datafile)

            # create Car objects per data row
            for row in datafile:
                car = Car(row[0], row[1], row[2], row[3], row[4])
                cars_list.append(car)

        return cars_list

    def create_layout(self):
        """
        Creates matrix of board with cars.
        """

        # create empty board matrix
        self.layout = np.chararray((self.size, self.size), unicode=True)
        self.layout[:] = '_'

        # place cars on board horizonally (H) or vertically (V)
        for car in self.cars:
            if car.orientation == "H":

                # place as many letters on board as car length
                self.layout[car.row, car.col:car.col + car.length] = car.name
            elif car.orientation == "V":
                self.layout[car.row:car.row + car.length, car.col] = car.name

        return self.layout

    def draw_board(self):
        """
        Prints board matrix on screen.
        """

        # clear screen for new board
        print("\033[H\033[J")

        # print new board
        for row in self.layout:
            for block in row:
                print(f"{block} ", end="")
            print("")

