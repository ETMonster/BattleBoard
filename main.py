from text import *
from enemy import enemy_configurations
import string
import random

board_height = 7
board_width = 7

class Board:
    def __init__(self, positions, healths, army, width, height):
        self.positions = positions
        self.healths = healths
        self.army = army
        self.width = width
        self.height = height

    def print_board(self, board, coordinates_in_range):
        print(' ', end='')
        for c in list(string.ascii_uppercase)[:self.width]:
            print(f'  {style.bold}{fore.blue}{c}{'  ' if board == self.healths else ''}', end='')

        print('')

        for i in range(self.height):
            print(f'{style.bold}{fore.blue}{i + 1}', end='')
            print('  ', end = '')
            for j in range(self.width):
                a = self.army[i][j]
                print(f'{style.none}'
                      f'{fore.magenta if [i, j] in coordinates_in_range else fore.green if a == 'U' else fore.red if a == 'E' else fore.white}'
                      f'{board[i][j]}'
                      f'{(' ' * ((3 - len(board[i][j])) + 2)) if board == self.healths else '  '}', end='')

            print('')

        print('')

    def print(self, coordinates_in_range):
        print(f'{style.bold}{fore.white}HEALTH BOARD')
        self.print_board(self.healths, coordinates_in_range)

        print(f'{style.bold}{fore.white}POSITION BOARD')
        self.print_board(self.positions, coordinates_in_range)

    def get_evaluation(self):
        s = 0

        for i in range(self.width):
            for j in range(self.height):
                if self.healths[i][j] != '-':
                    s += int(self.healths[i][j]) if self.army[i][j] == 'E' else -int(self.healths[i][j])

        return s

    def move_squadron(self, origin, desired):
        # Move origin attributes to desired position
        self.positions[desired[0]][desired[1]] = self.positions[origin[0]][origin[1]]
        self.healths[desired[0]][desired[1]] = self.healths[origin[0]][origin[1]]
        self.army[desired[0]][desired[1]] = self.army[origin[0]][origin[1]]

        # Remove existence of origin attributes
        self.positions[origin[0]][origin[1]] = '-'
        self.healths[origin[0]][origin[1]] = '-'
        self.army[origin[0]][origin[1]] = '-'

    def attack_squadron(self, squadron, desired):
        # Subtract health of squadron at a specific position based on its attacker's damage and bonus damage
        enemy_squadron = squadron_classes[self.positions[desired[0]][desired[1]]]
        bonus = False

        if enemy_squadron.name in squadron.bonus_against:
            bonus = True

        self.healths[desired[0]][desired[1]] = (str(int(self.healths[desired[0]][desired[1]]) - ((squadron.damage + squadron.bonus_damage) if bonus else squadron.damage)))

    def get_coordinates_in_range(self, origin, action, action_range):
        # Get the coordinates in a specified range of an origin point
        if action == 'm':
            return [[i, j] for i in range(self.width) for j in range(self.height)
                    if (abs(i - origin[0]) <= action_range and abs(j - origin[1]) <= action_range)
                    and action_range > 0 and self.army[i][j] == '-']
        elif action == 'a':
            return [[i, j] for i in range(self.width) for j in range(self.height)
                    if (abs(i - origin[0]) <= action_range and abs(j - origin[1]) <= action_range)
                    and action_range > 0 and self.army[i][j] == ('E' if self.army[origin[0]][origin[1]] == 'U' else 'U')]


class SquadronClass:
    def __init__(self, name, health, attack_range, move_range, damage, bonus_damage, bonus_against):
        self.name = name
        self.health = health
        self.attack_range = attack_range
        self.move_range = move_range
        self.damage = damage
        self.bonus_damage = bonus_damage
        self.bonus_against = bonus_against

squadron_classes = {
    'A': SquadronClass('Archer', 100, 4, 1, 60, 30, ['Spearman', 'Footman']),
    'F': SquadronClass('Footman', 350, 1, 2, 45, 30, ['Mage', 'Archer']),
    'S': SquadronClass('Spearman', 650, 1, 1, 10, 100, ['Cavalier', 'Footman']),
    'C': SquadronClass('Cavalier', 500, 1, 4, 50, 30, ['Archer', 'Mage']),
    'M': SquadronClass('Mage', 200, 3, 2, 30, 40, ['Spearman', 'Cavalier'])
}


def main():
    battle_squadrons = {
        'A': 2,
        'F': 3,
        'M': 1,
        'C': 2,
        'S': 1
    }

    battle(battle_squadrons)


def convert_display_to_coordinates(position):
    # Converts a display position into a board coordinate
    x = int(position[1]) - 1
    y = ord(position[0].lower()) - 97

    return [x, y]

def get_position_input(board):
    # Returns a valid display position, board coordinate, and whether the spot is taken
    while True:
        result = input()
        taken = True
        is_enemy = True

        if len(result) == 2:
            if result[0] in string.ascii_uppercase[:board.width] and result[1] in str(list(range(1, board.height + 1))):

                coordinates = convert_display_to_coordinates(result)

                if board.positions[coordinates[0]][coordinates[1]] == '-':
                    taken = False

                if board.army[coordinates[0]][coordinates[1]] != 'E':
                    is_enemy = False

                return [result, coordinates, taken, is_enemy]

def battle_user_turn(board):
    print(f'{style.under}{fore.white}USER TURN{style.none}{fore.white}')

    board.print([])

    print(f'{style.none}{fore.white}Move a friendly squadron ({fore.cyan}m{fore.white}) OR attack an enemy squadron ({fore.cyan}a{fore.white})')

    # Get action that user desires to make
    action = input()

    while action != 'm' and action != 'a':
        action = input()

    print(f'{style.none}{fore.white}From what position would you like to {'move' if action == 'm' else 'attack'}?')

    origin_display = ''
    origin_coordinates = []
    origin_taken = False
    origin_is_enemy = False

    while not origin_taken or origin_is_enemy:
        origin_input = get_position_input(board)

        origin_display = origin_input[0]
        origin_coordinates = origin_input[1]
        origin_taken = origin_input[2]
        origin_is_enemy = origin_input[3]

    # Get the squadron attributes at the specified position
    squadron = squadron_classes[board.positions[origin_coordinates[0]][origin_coordinates[1]]]

    if action == 'm':
        # Get the coordinates in range for the squadron to move to
        coordinates_in_range = board.get_coordinates_in_range(origin_coordinates, 'm', squadron.move_range)

        # Check if there are no possible movements
        if len(coordinates_in_range) == 0:
            print(f'{style.none}{fore.white}No possible moves for squadron at {origin_display}. Try a different action or squadron.\n')
            battle_user_turn(board)

        # Get desired movement destination
        board.print(coordinates_in_range)

        print(f'{style.none}{fore.white}To what position in the specified range would you like to move?')

        next_display = ''
        next_coordinates = []
        next_taken = True
        next_in_range = False

        while next_taken or not next_in_range:
            next_input = get_position_input(board)

            next_display = next_input[0]
            next_coordinates = next_input[1]
            next_taken = next_input[2]
            next_in_range = True if next_coordinates in coordinates_in_range else False

        # Move squadron
        board.move_squadron(origin_coordinates, next_coordinates)

        board.print([])

        print(f'{fore.green}{style.bold}{squadron.name}{style.none}{fore.white} squadron has moved: {fore.blue}{style.bold}{origin_display} - {next_display}{style.none}{fore.white}')

    if action == 'a':
        # Get the coordinates in range for the squadron to attack
        coordinates_in_range = board.get_coordinates_in_range(origin_coordinates, 'a', squadron.attack_range)

        # Check if there are possible attacks
        if len(coordinates_in_range) == 0:
            print(f'{style.none}{fore.white}No possible attacks for squadron at {origin_display}. Try a different action or squadron.\n')
            battle_user_turn(board)

        # Get desired enemy to attack
        board.print(coordinates_in_range)

        print(f'{style.none}{fore.white}What enemy in the specified range would you like to attack?')

        next_display = ''
        next_coordinates = []
        next_is_enemy = False
        next_in_range = False

        while not next_is_enemy or not next_in_range:
            next_input = get_position_input(board)

            next_display = next_input[0]
            next_coordinates = next_input[1]
            next_is_enemy = next_input[3]
            next_in_range = True if next_coordinates in coordinates_in_range else False

        # Attack enemy squadron
        board.attack_squadron(squadron, next_coordinates)

    battle_user_turn((minimax(board, 3, float('-inf'), float('inf'), True))[1])


def battle(user_squadrons):
    # Generate an empty board
    board = Board(
        [['-' for _ in range(board_width)]for _ in range(board_height)],
        [['-' for _ in range(board_width)]for _ in range(board_height)],
        [['-' for _ in range(board_width)]for _ in range(board_height)],
        board_width, board_height
    )

    # Make a random pre-made enemy army configuration on the board
    enemy_configuration = enemy_configurations[random.randrange(0, len(enemy_configurations))]

    board.positions = enemy_configuration
    board.healths = [[str(squadron_classes[y].health) if y in squadron_classes else '-' for y in x] for x in board.positions]
    board.army = [['E' if y != '-' else '-' for y in x] for x in board.positions]

    board.print([])

    # Choose starting configuration
    for key in user_squadrons:
        for i in range(user_squadrons[key]):
            print(f'{style.none}{fore.white}Choose a position for {style.bold}{fore.green}{squadron_classes[key].name}{style.none}{fore.white} #{i + 1}.')
            display = ''
            coordinates = []
            position_taken = True

            while position_taken:
                position_input = get_position_input(board)

                display = position_input[0]
                coordinates = position_input[1]
                position_taken = position_input[2]

            board.positions[coordinates[0]][coordinates[1]] = key
            board.healths[coordinates[0]][coordinates[1]] = str(squadron_classes[key].health)
            board.army[coordinates[0]][coordinates[1]] = 'U'

            print('')
            board.print([])

            print(f'{style.none}{fore.white}Imported {style.bold}{fore.green}{squadron_classes[key].name}{style.none}{fore.white} #{i + 1} at {style.bold}{fore.blue}{display}{style.none}{fore.white}.')

    # Battle!

    battle_user_turn(board)


# Enemy AI using minimax and alpha-beta pruning algorithms
def get_board_children(parent, enemy_turn):
    # Declare variables depending on who's turn it is
    army = 'E' if enemy_turn else 'U'
    children = []

    # Loop through all squadrons
    for i in range(parent.width):
        for j in range(parent.height):
            if parent.army[i][j] != army:
                continue

            # Loop through each possible coordinate in the move or attack range for one squadron
            squadron = squadron_classes[parent.positions[i][j]]

            for coordinate in parent.get_coordinates_in_range([i, j], 'a', squadron.attack_range):
                child = Board(
                    [[y for y in x] for x in parent.positions],
                    [[y for y in x] for x in parent.healths],
                    [[y for y in x] for x in parent.army],
                    parent.width, parent.height
                )

                child.attack_squadron(squadron, coordinate)

                children.append(child)

            for coordinate in parent.get_coordinates_in_range([i, j], 'm', squadron.move_range):
                child = Board(
                    [[y for y in x] for x in parent.positions],
                    [[y for y in x] for x in parent.healths],
                    [[y for y in x] for x in parent.army],
                    parent.width, parent.height
                )

                child.move_squadron([i, j], coordinate)

                children.append(child)

    return children

def minimax(board, depth, alpha, beta, enemy_turn):
    # A minimax algorithm using recursive functions to iterate through all possible moves of a parent board.
    # If depth is zero or game is over in that board then it returns the static evaluation of the current child board to its parent board.

    #or """game over in this board"""
    if depth == 0:
        return board.get_evaluation(), board

    children = get_board_children(board, enemy_turn)

    # Depending on who's turn it is in the prediction, get all children of the current board (1 move into the future
    # for one team) and return the best evaluation for that team. The enemy AI chooses the best move depending on the
    # algorithm's depth.
    if enemy_turn:
        max_evaluation = float('-inf')
        best_child = None
        for child in children:
            evaluation, _ = minimax(child, depth - 1, alpha, beta, False)
            #print(f"Evaluating child: {child}, Evaluation: {evaluation}")
            if evaluation > max_evaluation:
                max_evaluation = evaluation
                best_child = child

            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break

        return max_evaluation, best_child

    else:
        min_evaluation = float('inf')
        best_child = None
        for child in children:
            evaluation, _ = minimax(child, depth - 1, alpha, beta, True)
            if evaluation < min_evaluation:
                min_evaluation = evaluation
                best_child = child

            beta = min(beta, evaluation)
            if beta <= alpha:
                break

        return min_evaluation, best_child

main()