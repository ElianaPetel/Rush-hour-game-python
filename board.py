class Board:
    """
    Represents the game board.
    """

    def __init__(self):
        # Initialize the game board as a 7x7 grid filled with empty spaces
        self.board = [["_" if j < 7 else "*" for j in range(8)] for i in range(7)]

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        # The game may assume this function returns a reasonable representation
        # of the board for printing, but may not assume details about it.
        board_str = ""
        for row in self.board:
            board_str += " ".join(row) + "\n"
        return board_str

    def cell_list(self):
        """This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        coordinates = []
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                coordinates.append((row, col))
        coordinates.append((3, 7))
        return coordinates

    def get_car_orientation(self, car_locations):
        # Check if all coordinates have the same row (horizontal orientation)
        if all(coord[0] == car_locations[0][0] for coord in car_locations):
            return 1
        # Check if all coordinates have the same column (vertical orientation)
        elif all(coord[1] == car_locations[0][1] for coord in car_locations):
            return 0
        else:
            return "invalid"  # If neither vertical nor horizontal

    def can_move_left(self, car_locations):
        # Check if the car can move left (decreasing columns by one)
        if 0 < car_locations[0][1]:
            # Check if the cell left of the car is empty
            if self.board[car_locations[0][0]][car_locations[0][1] - 1] != "_":
                return False
            return True
        return False

    def can_move_right(self, car_locations):
        # Check if the car can move right (increasing columns by one)
        if car_locations[-1][1] < 6:
            # Check if the cell right of the car is empty
            if self.board[car_locations[-1][0]][car_locations[-1][1] + 1] != "_":
                return False
            return True
        # if car is behind the winning cell
        elif car_locations[-1] == (3, 6):
            return True
        return False

    def can_move_up(self, car_locations):
        # Check if the car can move up (decreasing rows by one)
        if 0 < car_locations[0][0]:
            # Check if the cell above the car is empty
            if self.board[car_locations[0][0] - 1][car_locations[0][0]] != "_":
                return False
            return True
        return False

    def can_move_down(self, car_locations):
        # Check if the car can move down (increasing rows by one)
        if car_locations[-1][0] < 6:
            # Check if the cell above the car is empty
            if self.board[car_locations[-1][0] + 1][car_locations[-1][1]] != "_":
                return False
            return True
        return False

    def get_cars_info(self):
        """Collects information about the cars on the board
        and regroups them inside a dictionnary"""
        # Initialize a dictionary to store car locations and lengths
        car_info = {}
        # Iterate over the board and collect car locations and lengths
        for row in range(7):
            for col in range(7):
                car_name = self.board[row][col]
                if car_name != "_":
                    if car_name not in car_info:
                        car_info[car_name] = {"locations": [], "length": 1}
                    else:
                        car_info[car_name]["length"] += 1
                    car_info[car_name]["locations"].append((row, col))
        return car_info

    def possible_moves(self):
        """This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,move_key,description)
                 representing legal moves
        """
        legal_moves = []
        car_info = self.get_cars_info()
        for car_name, info in car_info.items():
            car_locations = info["locations"]
            car_orientation = self.get_car_orientation(car_locations)
            # Check possible moves based on orientation and length
            if car_orientation == 1:
                if self.can_move_left(car_locations):
                    legal_moves.append((car_name, "l", "Move left"))
                if self.can_move_right(car_locations):
                    legal_moves.append((car_name, "r", "Move right"))
            elif car_orientation == 0:
                if self.can_move_up(car_locations):
                    legal_moves.append((car_name, "u", "Move up"))
                if self.can_move_down(car_locations):
                    legal_moves.append((car_name, "d", "Move down"))
        # Now legal_moves contains all the valid moves for cars on the board
        return legal_moves

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        return (3, 7)

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        row, col = coordinate
        if 0 <= row < 7 and 0 <= col < 7:
            if self.board[row][col] == "_":
                return None
            else:
                return self.board[row][col]
        elif (row, col) == (3, 7):
            if self.board[3][7] == "*":
                return None
            else:
                return self.board[3][7]  # Return the car_name for the special case

    def add_car(self, car_inst):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        # Remember to consider all the reasons adding a car can fail.
        # You may assume the car is a legal car object following the API.
        # Check if the car fits within the board boundaries
        if car_inst.orientation == 0:  # Vertical orientation
            if (
                car_inst.location[0] + car_inst.length > 7
                or car_inst.location[0] < 0
                or car_inst.location[1] < 0
                or car_inst.location[1] > 7
            ):
                return False
        elif car_inst.orientation == 1:  # Horizontal orientation
            if (
                car_inst.location[1] + car_inst.length > 7
                or car_inst.location[1] < 0
                or car_inst.location[0] < 0
                or car_inst.location[0] > 7
            ):
                return False
        for cell in self.cell_list():
            if car_inst.name == self.cell_content(cell):
                return False
        # Check if the car's location is occupied by another car
        for coord in car_inst.car_coordinates():
            if self.cell_content(coord) != None:
                return False

        # If all checks pass, add the car to the board
        for coord in car_inst.car_coordinates():
            row, col = coord
            self.board[row][col] = car_inst.name
        return True

    def calculate_new_coordinates(self, car_locations, move_key):
        # Calculate new coordinates after a valid move
        new_coordinates = []
        for row, col in car_locations:
            if move_key == "u":
                new_coordinates.append((row - 1, col))
            elif move_key == "d":
                new_coordinates.append((row + 1, col))
            elif move_key == "l":
                new_coordinates.append((row, col - 1))
            elif move_key == "r":
                new_coordinates.append((row, col + 1))
        return new_coordinates

    def is_valid_new_coordinates(self, new_coordinates):
        # Check if the new coordinates are valid (within the board and empty)
        for row, col in new_coordinates:
            print((row, col))
            if not (0 <= row < 7) or not (0 <= col < 7):
                if new_coordinates[-1] == (3, 7):
                    return True
                return False
        return True

    def update_board(self, old_coordinates, new_coordinates, name):
        # Update the board with the new coordinates
        for row, col in old_coordinates:
            self.board[row][col] = "_"
        for row, col in new_coordinates:
            self.board[row][col] = name

    def is_valid_move(self, car_locations, move_key):
        # Check if the move is valid for a given car
        if move_key == "u":
            return self.can_move_up(car_locations)
        elif move_key == "d":
            return self.can_move_down(car_locations)
        elif move_key == "l":
            return self.can_move_left(car_locations)
        elif move_key == "r":
            return self.can_move_right(car_locations)
        return False

    def move_car(self, name, move_key):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param move_key: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        cars_info = self.get_cars_info()
        if not cars_info:
            return False

        car_to_move = cars_info.get(name)
        if car_to_move is None:
            return False

        car_locations = car_to_move["locations"]
        if not self.is_valid_move(car_locations, move_key):
            return False

        new_coordinates = self.calculate_new_coordinates(car_locations, move_key)
        if self.is_valid_new_coordinates(new_coordinates):
            self.update_board(car_locations, new_coordinates, name)

            return True
        return False
