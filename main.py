import csv
import time
import copy
import sys

from code.algorithms.random import random_move
from code.classes.board import Board
from code.classes.car import Car
from code.classes.game import Game

sys.setrecursionlimit(10000)

boardMemory = []
boardMemoryMoves = []
quickestWin = 250

def solve(game, amountOfMoves, moveList):
    global quickestWin
    amountOfMoves += 1
    if amountOfMoves < quickestWin:
        amountOfPossibleMoves = len(game.find_moves())
        for i in range(amountOfPossibleMoves):
            gameCopy = copy.deepcopy(game)
            moves = gameCopy.find_moves()
            move = moves[i]
            gameCopy.move(move)
            gameCopy.board.create_layout()
            conti = True
            if gameCopy.board.cars in boardMemory:
                i = boardMemory.index(gameCopy.board.cars)
                if boardMemoryMoves[i] > amountOfMoves:
                    boardMemoryMoves[i] = amountOfMoves
                else:
                    conti = False
            else:
                boardMemory.append(gameCopy.board.cars)
                boardMemoryMoves.append(amountOfMoves)
            if conti:
                if gameCopy.win():
                    quickestWin = amountOfMoves
                    print("WE WONNN!!!! in " + str(amountOfMoves) + " moves!" )
                    c = moveList[:]
                    c.append(str(move[0].name) +"," + str(move[1]))
                    print(c)
                    game.board.draw_board()
                else:
                    b = moveList[:]
                    b.append(str(move[0].name) +"," + str(move[1]))
                    solve(gameCopy, amountOfMoves, b)


if __name__ == '__main__':

    # initialize best moves list
    best_moves = [None] * 100000

    # play game untill interrupted with ctrl-c
    try:
        # while True:
        # create new game
        game = Game('data/Rushhour6x6_1.csv')

        # draw first board
        game.board.draw_board()

        # keep track of time
        t0 = time.perf_counter()


        solve(game, 0, [])

        # # make random moves until win
        # while not game.win() and len(game.moves) <= len(best_moves):
        #
        #     # find possible moves
        #     valid_moves = game.find_moves()
        #
        #     # use random algorithm to choose moves
        #     choice = random_move(valid_moves)
        #
        #     # move car and create new layout
        #     game.move(choice)
        #     game.board.create_layout()




        # # draw final board
        # game.board.draw_board()
        #
        # # stop time
        # t1 = time.perf_counter() - t0
        #
        # #print number of played moves, time elapsed and speed
        # print(f"{len(game.moves)} in {t1:.2f} s")
        # print(f"{len(game.moves)/t1:.1f} moves/s")

        # update best moves list when new list is smaller
        # if len(game.moves) < len(best_moves):
        #     best_moves = game.moves

    except KeyboardInterrupt:

        # write output
        with open('output.csv', 'w', newline='') as outputfile:
            fieldnames = ['car', 'move']
            writer = csv.writer(outputfile)
            writer.writerow(fieldnames)
            writer.writerows(best_moves)


