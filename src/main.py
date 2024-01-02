'''
File: main.py
Auth: Blake Wingard - bats23456789@gmail.com
Date: 12/30/2024
Desc: The main entry point for the project.
'''
import battleship


def main():
    board = battleship.Board()
    board.addShip(battleship.Ship('Carrier', (0, 0), (0, 4)))

    try:
        board.addShip(battleship.Ship('Battleship', (0, 0), (0, 3)))
    except battleship.OverlapException:
        print('Overlapping ships')

    board.addShip(battleship.Ship('Battleship', (1, 0), (4, 0)))

    try:
        board.addShip(battleship.Ship('Destroyer', (1, 2), (4, 1)))
    except battleship.InvalidPlacementException:
        print('Diagonal placement')

    board.addShip(battleship.Ship('Destroyer', (2, 2), (4, 2)))

    try:
        board.addShip(battleship.Ship('Submarine', (2, 10), (4, 10)))
    except battleship.OutOfBoundsException:
        print('Out of bounds')

    board.addShip(battleship.Ship('Submarine', (4, 9), (6, 9)))
    board.removeShip('Submarine')

    print(board)

    shot = (0, 0)

    print(f'{shot}: {board.shoot(shot)}')
    print(f'{shot}: {board.shoot(shot)}')
    shot = (1, 1)
    print(f'{shot}: {board.shoot(shot)}')
    print(board)

    for i in range(1, 5):
        shot = (0, i)
        board.shoot(shot)

    print(board)

    print(f'GameOver: {board.isGameOver()}')

    for i in range(0, 4):
        shot = (1 + i, 0)
        board.shoot(shot)

    for i in range(0, 3):
        shot = (2 + i, 2)
        board.shoot(shot)

    for i in range(0, 3):
        shot = (4 + i, 9)
        board.shoot(shot)

    print(board)

    print(f'GameOver: {board.isGameOver()}')

    return 0


if __name__ == '__main__':
    main()
