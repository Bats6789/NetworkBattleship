'''
File: main.py
Auth: Blake Wingard - bats23456789@gmail.com
Date: 12/30/2024
Desc: The main entry point for the project.
'''
from battleship import Board
from battleship import Ship
import battleship
# from gameView import GameView
from setupView import SetupView
import sys
from PyQt6.QtWidgets import QApplication


def parseInput():
    done = False
    while not done:
        data = input()
        if (len(data) != 2 and len(data) != 3):
            print('Please enter in the letter-number format. Ex. B4')
        elif not data[0].isalpha() or not data[1:].isnumeric():
            print('Please enter in the letter-number format. Ex. B4')
        elif 'A' > data[0] or data[0] > 'J':
            print('Letter is out of range. Can only be between "A" and "J"')
        elif int(data[1:]) < 0 or int(data[1:]) > 10:
            print('Number is out of range. Can only be between "1" and "10"')
        else:
            pos = (int(data[1:] - 1, ord(data[0].upper()) - ord('A')))
            done = True

    return pos


def getShipFromPlayer(playerName: str, shipName: str, length: int) -> Ship:
    done = False
    while not done:
        print(f'{playerName}, enter the start coordinates for the {shipName}: ')
        start = parseInput()
        print(f'{playerName}, enter the stop coordinates for the {shipName}: ')
        stop = parseInput()

        try:
            ship = Ship(shipName, start, stop)
        except battleship.InvalidPlacementException:
            print('Ship can not be diagonal')
            print('Please try again')
            continue

        if len(ship) != length:
            print('Ship is too small')
        else:
            done = True

    return ship


def quickSetup() -> Board:
    board = Board()

    # Carrier
    board.addShip(Ship('Carrier', (0, 0), (0, 5)))

    # Battleship
    board.addShip(Ship('Battleship', (1, 0), (1, 4)))

    # Destroyer
    board.addShip(Ship('Destroyer', (2, 0), (2, 3)))

    # Submarine
    board.addShip(Ship('Submarine', (3, 0), (3, 3)))

    # Patrol Boat
    board.addShip(Ship('Patrol Boat', (4, 0), (4, 2)))

    return board


def setupPlayer(playerName: str) -> Board:
    board = Board()

    def addShipToBoard(shipName: str, length: int):
        done = False
        while not done:
            try:
                board.addShip(getShipFromPlayer(playerName, shipName, length))
            except battleship.OverlapException:
                print('Ships can not overlap')
                print('Please try again')
            except battleship.OutOfBoundsException:
                print('The ship does not fit on the board')
                print('Please try again')
            else:
                done = True

    # Carrier
    addShipToBoard('Carrier', 5)

    # Battleship
    addShipToBoard('Battleship', 4)

    # Destroyer
    addShipToBoard('Destroyer', 3)

    # Submarine
    addShipToBoard('Submarine', 3)

    # Patrol Boat
    addShipToBoard('Patrol Boat', 2)

    return board


def attemptShot(player: Board):
    done = False

    while not done:
        print('Enter shot location:')
        shot = parseInput()

        try:
            results = player.shoot(shot)
        except battleship.OutOfBoundsException:
            print('Shot is out of bounds')
        else:
            if results == 'SAME':
                print('Already shot at this location')
                print('Please try again\n')
            else:
                if results == 'SUNK':
                    print(f'You sunk my {player.getShipAtPos(shot)}')
                else:
                    print(results)
                done = True


class Grid:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 100
        self.h = 100


def main():
    # player1 = setupPlayer('Player 1')
    # player1 = quickSetup()
    # player2 = setupPlayer('Player 2')
    # gameOver = False
    # turnPlayer = 1
    #
    # print('Player 1:')
    # print(player1)
    #
    # print()
    #
    # print('Player 2:')
    # print(player2)
    #
    # print()
    #
    # while not gameOver:
    #
    #     if turnPlayer == 1:
    #         print('Player 1\'s turn')
    #         attemptShot(player2)
    #         turnPlayer = 2
    #     else:
    #         print('Player 2\'s turn')
    #         attemptShot(player1)
    #         turnPlayer = 1
    #     print()
    #
    #     gameOver = player1.isGameOver() or player2.isGameOver()
    #
    # if player1.isGameOver():
    #     print('Player 2 Wins!')
    # else:
    #     print('Player 1 Wins!')

    app = QApplication(sys.argv)

    # window = GameView(player1)
    window = SetupView()
    window.show()

    app.exec()

    return 0


if __name__ == '__main__':
    main()
