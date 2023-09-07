import board
import car
import helper


class Game:
    """
    Represents the game manager.
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        # You may assume board follows the API
        self.board = board
        self.game_over = False
        self.quit_game = False
        self.winner = None
        self.cars = []
        # list containing all the car instances on the board

    def check_input_validity(self, move_input):
        """
        Parse the move input into car name and move key.
        :param move_input: A string containing the move input.
        :return: A tuple (car_name, move_key) or None if invalid input.
        """
        move_input = move_input.split(",")
        if len(move_input) != 2:
            print("Invalid input. Please enter move as 'car_name,move_key'.")
            return None
        return tuple(move_input)

    def find_car_instance(self, car_name):
        """
        Find a car instance by name.
        :param car_name: The name of the car to find.
        :return: The car instance or None if not found.
        """
        for car_inst in self.cars:
            if car_inst.name == car_name:
                return car_inst
        return None

    def is_valid_move(self, car_instance, car_name, move_key):
        """
        Check if the requested move is valid for the given car.
        :param car_name: The name of the car to move.
        :param move_key: The move key (e.g., 'u', 'd', 'l', 'r').
        :return: True if the move is valid, False otherwise.
        """
        valid_car_moves = car_instance.possible_moves()
        if move_key not in valid_car_moves.keys():
            print("The car can not move in this direction. Please enter a valid move.")
            return False

        valid_moves_on_board = self.board.possible_moves()
        if (car_name, move_key) not in [move[:2] for move in valid_moves_on_board]:
            print("This move is invalid on this board. Please enter a valid move.")
            return False

        return True

    def move_car(self, car_instance, car_name, move_key):
        """
        Move the car on the board if the move is valid.
        :param car_instance: The instance of the Car class.
        :param car_name: The name of the car to move.
        :param move_key: The move key (e.g., 'u', 'd', 'l', 'r').
        :return: True if the move was successful, False otherwise.
        """
        success = self.board.move_car(car_name, move_key)
        if success:
            if move_key == "u":
                car_instance.location = (
                    car_instance.location[0] - 1,
                    car_instance.location[1],
                )
            elif move_key == "d":
                car_instance.location = (
                    car_instance.location[0] + 1,
                    car_instance.location[1],
                )
            elif move_key == "l":
                car_instance.location = (
                    car_instance.location[0],
                    car_instance.location[1] - 1,
                )
            elif move_key == "r":
                car_instance.location = (
                    car_instance.location[0],
                    car_instance.location[1] + 1,
                )
            print(f"Moved {car_name} {move_key}")
            print(self.board.__str__())
        else:
            print("Invalid move. Please enter a valid move.")
        return success

    def __single_turn(self):
        """
        The function runs one round of the game.
        """
        move_input = input("Enter move as 'car_name,move_key': ")
        if move_input == "!":
            self.quit_game = True
        else:
            # check input validity
            move_input = self.check_input_validity(move_input)
            if move_input is not None:
                car_name, move_key = move_input
                # Iterate through the car instances and look for the desired car to move
                car_instance = self.find_car_instance(car_name)
                if car_instance is None:
                    print(f"Car {car_name} Does not exist.")
                    return
                else:
                    # if victory, end the game
                    if (
                        car_instance.orientation == 1
                        and car_instance.location[0] == 3
                        and car_instance.location[1] + car_instance.length == 7
                        and move_key == "r"
                    ):
                        self.game_over = True
                        self.winner = car_name
                    else:
                        # check validity of required move, avoiding errors as early as possible
                        if self.is_valid_move(car_instance, car_name, move_key) == True:
                            self.move_car(car_instance, car_name, move_key)

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        while not self.game_over and not self.quit_game:
            self.__single_turn()
        if self.winner:
            print(f"Congratulations! The {self.winner} car has reached the exit.")
        elif self.quit_game:
            print("Game has been quit.")


if __name__ == "__main__":
    # Create a new game
    game_board = board.Board()
    game_instance = Game(game_board)

    # Load car configurations from the JSON file
    car_config = helper.load_json("car_config.json")

    # Create and add cars to the game board
    for name, config in car_config.items():
        length, location, orientation = config
        location = tuple(location)
        car_instance = car.Car(name, length, location, orientation)
        is_car_added = game_board.add_car(car_instance)
        if is_car_added:
            game_instance.cars.append(car_instance)
        else:
            print(f"Failed to add car {name} to the board.")
    # Start the game
    print(game_board.__str__())
    game_instance.play()
