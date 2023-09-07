class Car:
    """
    Represents a car on the game board.
    """

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        self.name = name
        self.length = length
        self.location = location
        self.orientation = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        if self.orientation == 0:
            coordinates = [
                (self.location[0] + i, self.location[1]) for i in range(self.length)
            ]
        else:
            coordinates = [
                (self.location[0], self.location[1] + i) for i in range(self.length)
            ]
        return coordinates

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        if self.orientation == 0:
            moves = {
                "u": "causes the car to move upward",
                "d": "causes the car to move downward",
            }
        elif self.orientation == 1:
            moves = {
                "l": "causes the car to move leftward",
                "r": "causes the car to move rightward",
            }
        return moves

    def movement_requirements(self, move_key):
        """
        :param move_key: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """
        if move_key == "u":
            return [(self.location[0] - 1, self.location[1])]
        elif move_key == "d":
            return [(self.location[0] + self.length, self.location[1])]
        elif move_key == "l":
            return [(self.location[0], self.location[1] - 1)]
        elif move_key == "r":
            return [(self.location[0], self.location[1] + self.length)]
        else:
            return None

    def move(self, move_key):
        """
        :param move_key: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        requirements = self.movement_requirements(move_key)
        if requirements != None:
            if (
                self.orientation == 1
                and move_key not in ("l", "r")
                or self.orientation == 0
                and move_key not in ("u", "d")
            ):
                return False
            else:
                return True
        else:
            return False

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.name
