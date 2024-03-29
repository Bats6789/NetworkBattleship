'''
File: battleship.py
Auth: Blake Wingard - bats23456789@gmail.com
Date: 01/02/2024
Desc: Game logic for battleship.
'''


class OutOfBoundsException(Exception):
    'Raised when a ship is out of bounds'
    pass


class InvalidPlacementException(Exception):
    'Raised when the ship is placed diagonally'
    pass


class OverlapException(Exception):
    'Raised when the ship overlaps another ship'
    pass


class Ship:
    '''
    A class to represent a Battleship Ship.

    Attributes
    ----------
    name: str
        The grid on the board containing ships and shots

    start: tuple[int, int]
        Stores the ships start coordinates

    stop: tuple[int, int]
        Stores the ships stop coordinates

    Methods
    -------
    shoot(shot): bool
        Attempts to shoot the ship

    isSunk(): bool
        Checks if ship is sunk

    posOnShip: bool
        Checks if the position is on the ship
    '''

    def __init__(self, name: str, start: tuple[int, int], stop: tuple[int, int]):
        '''
        Constructs all the necesarry attributes for the Ship object

        Parameters
        ----------
        name: str
            The name of the ship

        start: tuple[int, int]
            The start coordinate of the ship

        stop: tuple[int, int]
            The stop coordinate of the ship
        '''
        if start[0] != stop[0] and start[1] != stop[1]:
            raise InvalidPlacementException

        self.name = name
        self.start = start
        self.stop = stop

        if start[0] == stop[0]:
            self.hits = [False for i in range(start[1], stop[1] + 1)]
        else:
            self.hits = [False for i in range(start[0], stop[0] + 1)]

    def __repr__(self):
        '''
        Displays a string representation of the Ship Object
        '''
        return f'{self.name}: {self.start}-{self.stop}: '\
            f'[{"".join("X" if shot else "O" for shot in self.hits)}]'

    def __len__(self):
        '''
        Gives the length of the ship
        '''
        return len(self.hits)

    def shoot(self, shot: tuple[int, int]) -> bool:
        '''
        Attempts to shoot the ship

        A shot hits a ship if the position of the shot is within
        the boundaries of the start and stop (inclusive) of the ship

        Parameters
        ----------
        shot: tuple[int, int]
            The position of the shot

        Returns
        -------
        bool: True if shot hit ship
        '''
        if self.posOnShip(shot):
            key = shot[0] - self.start[0] + shot[1] - self.start[1]
            self.hits[key] = True
            return True
        else:
            return False

    def isSunk(self) -> bool:
        '''
        Checks if ship is sunk

        A ship is sunk when all integer positions between the
        start and stop (inclusive) have been hit

        Returns
        -------
        bool: True if all positions are hit
        '''
        return all(self.hits)

    def posOnShip(self, pos: tuple[int, int]) -> bool:
        '''
        Checks if the position is on the ship

        Parameters
        ----------
        pos: tuple[int, int]
            The position to check

        Returns
        -------
        bool: True if the position is on the ship
        '''
        return self.start[0] <= pos[0] <= self.stop[0]\
            and self.start[1] <= pos[1] <= self.stop[1]


class Board:
    '''
    A class to represent a Battleship Board.

    Attributes
    ----------
    grid: list[list[int | str]]
        The grid on the board containing ships and shots

    ships: list[Ship]
        Stores the ships on the board

    Methods
    -------
    shipOverlap(ship): bool
        Checks if the ship will overlap any ships on the board

    isOutOfBounds(pos): bool
        Checks if the pos is out of bounds of the board

    addShip(ship):
        Attempts to add a ship to the board

    removeShip(): bool
        Attempts to remove ship from the board

    shoot(shot): str
        Shoots the specified location and reports hit, miss, or same

    isGameOver(): bool
        Checks if game is over.
    '''

    def __init__(self):
        '''
        Constructs all the necesarry attributes for the Board object
        '''
        self.grid = [[0 for i in range(10)] for j in range(10)]
        self.ships = []

    def __repr__(self) -> str:
        '''
        Displays a string representation of the Board Object
        '''
        return ' ' * 3 + ', '.join(str(i + 1) for i in range(0, 10)) + '\n'\
            + '\n'.join(f'{chr(i + ord("A"))}: ' + ', '.join(map(str, row))
                        for i, row in enumerate(self.grid)) + '\n'\
            + '\n'.join(str(ship) for ship in self.ships)

    def shipOverlap(self, ship: Ship) -> bool:
        '''
        Checks if the ship will overlap any ships on the board

        Parameters
        ----------
        ship: Ship
            The ship to check

        Returns
        -------
        bool: True if the ship overlaps
        '''
        for i in range(ship.start[0], ship.stop[0] + 1):
            for j in range(ship.start[1], ship.stop[1] + 1):
                if self.grid[j][i] != 0:
                    return True
        return False

    def isOutOfBounds(self, pos: tuple[int, int]) -> bool:
        '''
        Checks if the pos is out of bounds of the board

        Parameters
        ----------
        pos: tuple[int, int]
            The position to check

        Returns
        -------
        bool: True if pos is out of bounds
        '''
        return pos[0] < 0 or pos[0] >= 10 or pos[1] < 0 or pos[1] >= 10

    def addShip(self, ship: Ship):
        '''
        Attempts to add a ship to the board

        Ships are only added if there locations do not overlap
        another ship.

        Ships with duplicate names can be added.

        Parameters
        ----------
        ship: Ship
            The ship to add

        Raises
        ------
        OutOfBoundsException: The ship is out of bounds of the board
        OverlapException: The ship overlaps another ship
        '''
        if self.isOutOfBounds(ship.start) or self.isOutOfBounds(ship.stop):
            raise OutOfBoundsException

        if self.shipOverlap(ship):
            raise OverlapException

        self.ships.append(ship)

        for i in range(ship.start[0], ship.stop[0] + 1):
            for j in range(ship.start[1], ship.stop[1] + 1):
                self.grid[j][i] = ship.name[0]

    def removeShip(self, name: str) -> bool:
        '''
        Attempts to remove ship from the board

        If a duplicate exists, the first occurance will be removed

        Parameters
        ----------
        name: str
            The name of the ship to remove

        Returns
        -------
        bool: True if the ship was removed
        '''
        for ship in self.ships:
            if name == ship.name:
                for i in range(ship.start[0], ship.stop[0] + 1):
                    for j in range(ship.start[1], ship.stop[1] + 1):
                        self.grid[j][i] = 0
                self.ships.remove(ship)
                return True

        return False

    def strToPoint(self, s: str) -> tuple[int, int]:
        row = ord(s[0]) - ord('A')
        col = int(s[1:]) - 1
        return (col, row)

    def shoot(self, shot: tuple[int, int] | str) -> str:
        '''
        Shoots the specified location and reports miss, same, hit, or sunk

        Parameters
        ----------
        shot: tuple[int, int]
            The position of the shot in (x, y)
        shot: str
            The position of the shot as a string (e.g. B4)

        Returns
        -------
        str: "MISS" if the shot did not hit a ship
             "SAME" if the shot hit a previously shot position
             "HIT" if the shot hit a ship
             "SUNK" if the shot sank the ship

        Raises
        ------
        OutOfBoundsException: The shot is out of bounds of the board
        '''
        if isinstance(shot, str):
            shot = self.strToPoint(shot)

        if self.isOutOfBounds(shot):
            raise OutOfBoundsException

        didHit = 'ERROR'
        match(self.grid[shot[1]][shot[0]]):
            case 0:
                didHit = 'MISS'
            case 1:
                didHit = 'SAME'
            case _:
                for ship in self.ships:
                    if ship.shoot(shot):
                        if ship.isSunk():
                            didHit = 'SUNK'
                        else:
                            didHit = 'HIT'
                        break

        self.grid[shot[1]][shot[0]] = 1

        return didHit

    def isGameOver(self) -> bool:
        '''
        Checks if game is over.

        Returns
        -------
        bool: True if all ships have been sunk
        '''
        return all(map(Ship.isSunk, self.ships))

    def getShipAtPos(self, pos: tuple[int, int] | str) -> Ship | None:
        '''
        Gets a ship at position (pos) if it exists

        Parameters
        ----------
        pos: tuple[int, int]
            The position of the ship to find in (x, y)

        pos: str
            The position of the ship to find as a string (e.g. B4)

        Returns
        -------
        Ship: The ship found

        None: The ship was not found

        Exception
        ----------
        OutOfBoundsException: The shot is out of bounds of the board
        '''

        if isinstance(pos, str):
            pos = self.strToPoint(pos)

        if self.isOutOfBounds(pos):
            raise OutOfBoundsException

        if self.grid[pos[1]][pos[0]] == 0:
            return None

        foundShip = None

        for ship in self.ships:
            if ship.posOnShip(pos):
                foundShip = ship
                break

        return foundShip

    def isShot(self, pos: tuple[int, int] | str) -> bool:
        '''
        Checks if cell has been shot

        Parameters
        ----------
        pos: tuple[int, int]
            The position of the cell to check in (x, y)

        pos: str
            The position of the cell to check as a string (e.g. B4)

        Returns
        -------
        bool: True if the cell was shot

        Exception
        ----------
        OutOfBoundsException: The shot is out of bounds of the board
        '''
        if isinstance(pos, str):
            pos = self.strToPoint(pos)

        if self.isOutOfBounds(pos):
            raise OutOfBoundsException

        return self.grid[pos[1]][pos[0]] == 1
