import re, json
import sys, getopt
COORDINATES_REGEX = "^(\d+),(\d+)$"
COMMAND_REGEX = "^(GO) ([0-9]+)$|^(GO) ([0-9]+) (E|W|N|S)$|^(GO) ([a-z]+)$|^(GO) ([a-z]+) (E|W|N|S)$" \
                "|^(TURN) (left|right)$" # one of "GO 500", "GO 500 E", "GO park", "GO park N", "TURN left"
LANDMARKS_DICT = {"park": (5,10), "cafe": (10,10), "school": (10,15)}
DIRECTIONS = {"N": ("E", "W"), "W": ("N", "S"), "S": ("E", "W"), "E": ("N", "S")}

def get_start_coordinates(start_point_text):
    """
    :param start_point_text: x,y coordinates, both must be > 0
    :return: validated and converted to ints coordinates
    """
    # this function validates start_point and converts it to integers
    start_point = re.search(COORDINATES_REGEX, start_point_text)
    if not start_point:
        raise ValueError("Start point should be integers in format x,y")
    x, y = start_point.groups()
    x, y = int(x), int(y)
    if x < 0 or y < 0:
        raise ValueError("Start point x,y must be positive")
    return x, y

def parse_command(x, y, direction, command):
    """
    funcion that exacutes command and finds new coordinates and direction
    :param x: current x coordinate value
    :param y: current y coordinate value
    :param direction: current direction, one of "NWSE"
    :param command: DSL command, for example "GO 5 N" or "TURN left"
    :return: new combination of x, y, direction after command exacution
    """
    print(f"Parsing command '{command}'")
    #validate regex first
    command_items = re.search(COMMAND_REGEX, command)
    if not command_items:
        raise ValueError(f"Command '{command}' is not valid")
    command_items = [i for i in command_items.groups() if i is not None]
    if command_items[0] == "GO":
        destination = command_items[1]
        if destination.isdigit():
            # this is number of blocks to move
            distance = int(destination)
        else:
            # this is landmark, get distance to it
            if not destination in LANDMARKS_DICT:
                raise ValueError("Landmark '{destination}' does not exist.")
            # TODO: implement check for landmarks and calculation
            raise NotImplementedError()
        if len(command_items) == 3:
            #change direction before moving
            direction = command_items[2]
        # finally, move
        if direction is "E":
            x -= distance
        elif direction is "W":
            x += distance
        elif direction is "N":
            y += distance
        elif direction is "S":
            y -= distance
        if x < 0 or y < 0:
            raise ValueError("Route must not go out of grid, current coordinates are {}".format(x, y))
    else:
        #change direction
        if direction is None:
            raise ValueError("You cannot change direction in first place.")
        if command_items[1] == 'left':
            direction = DIRECTIONS[direction][0]
        else:
            direction = DIRECTIONS[direction][1]
    return x, y, direction

def process_path(routes_data, route_id):
    """
    This is main processor that triggers other functions
    :param routes_data: routes dict loaded from json file
    :param route_id: ID of route to calculate
    :return:
    """
    # get route data
    if route_id not in routes_data:
        #raise error if id is not there
        raise ValueError(f"Route ID {route_id} does not exist")
    route_data = routes_data[route_id]
    # get start point
    x, y = get_start_coordinates(route_data.pop(0))
    print(f"Starting point: {x}, {y}")
    direction = None
    # now parse instructions
    for command in route_data:
        x, y, direction = parse_command(x, y, direction, command)
        print(x, y, direction)
    print("END")
    #return end point of route
    return x,y

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["filepath=","route="])
    except getopt.GetoptError:
        print('routes.py -f <filepath> -r <route>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('routes.py -f <filepath> -r <route>')
            sys.exit()
        elif opt in ("-f", "--filepath"):
            filepath = arg
        elif opt in ("-r", "--route"):
            route = arg
    #open file
    with open(filepath) as data_file:
        routes_data = json.load(data_file)
    process_path(routes_data, route)

if __name__ == "__main__":
   main(sys.argv[1:])