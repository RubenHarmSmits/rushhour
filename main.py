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
    global boardMemory
    amountOfMoves += 1
    if amountOfMoves < quickestWin:
        moves = game.find_moves()
        for i in range(len(moves)):
            gamee = copy.deepcopy(game)
            moves = gamee.find_moves()
            move = moves[i]
            gamee.move(move)
            gamee.board.create_layout()
            conti = True
            if gamee.board.cars in boardMemory:
                i = boardMemory.index(gamee.board.cars)
                if boardMemoryMoves[i] > amountOfMoves:
                    boardMemoryMoves[i] = amountOfMoves
                else:
                    conti = False
            else:
                boardMemory.append(gamee.board.cars)
                boardMemoryMoves.append(amountOfMoves)
            if conti:
                if gamee.win():
                    quickestWin = amountOfMoves
                    print("WE WONNN!!!! in " + str(amountOfMoves) + " moves!" )
                    c = moveList[:]
                    c.append(str(move[0].name) +"," + str(move[1]))
                    print(c)
                    game.board.draw_board()
                else:
                    b = moveList[:]
                    b.append(str(move[0].name) +"," + str(move[1]))
                    solve(gamee, amountOfMoves, b)


if __name__ == '__main__':

    # initialize best moves list
    best_moves = [None] * 100000

    # play game untill interrupted with ctrl-c
    try:
        # while True:
        # create new game
        game = Game('data/Rushhour9x9_4.csv')

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


