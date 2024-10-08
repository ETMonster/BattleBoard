from text import *
import string

board_height = 9
board_width = 9

class Board:
    def __init__(self, positions, healths, army, height, width):
        self.positions = positions
        self.healths = healths
        self.army = army
        self.height = height
        self.width = width

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
                      f'{fore.green if a == 'U' else fore.red if a == 'E' else fore.magenta if [i, j] in coordinates_in_range else fore.white}'
                      f'{board[i][j]}'
                      f'{(' ' * ((3 - len(board[i][j])) + 2)) if board == self.healths else '  '}', end='')

            print('')

        print('')

    def print(self, coordinates_in_range):
        print(f'{style.bold}{fore.white}POSITION BOARD')
        self.print_board(self.positions, coordinates_in_range)

        print(f'{style.bold}{fore.white}HEALTH BOARD')
        self.print_board(self.healths, coordinates_in_range)

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
        'A': 1,
        'F': 1,
        'M': 0,
        'C': 0,
        'S': 0
    }

    battle(battle_squadrons, 0)

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


def get_coordinates_in_range(board, origin, action_range):
    return [[i, j] for i in range(board.width) for j in range(board.height) if (abs(i - origin[0]) <= action_range and abs(j - origin[1]) <= action_range) and action_range > 0]

def move_squadron(board, origin, desired):
    # Move origin attributes to desired position
    board.positions[desired[0]][desired[1]] = board.positions[origin[0]][origin[1]]
    board.healths[desired[0]][desired[1]] = board.healths[origin[0]][origin[1]]
    board.army[desired[0]][desired[1]] = board.army[origin[0]][origin[1]]

    # Remove existence of origin attributes
    board.positions[origin[0]][origin[1]] = '-'
    board.healths[origin[0]][origin[1]] = '-'
    board.army[origin[0]][origin[1]] = '-'

def attack_squadron(board, squadron, desired, bonus):
    board.healths[desired[0]][desired[1]] = str(int(board.healths[desired[0]][desired[1]]) - squadron.damage + squadron.bonus_damage if bonus else squadron.damage)

def battle_user_turn(board):
    print(f'{style.under}USER TURN{style.none}{fore.white}')

    board.print([])

    print(f'Move a friendly squadron ({fore.cyan}m{fore.white}) OR attack an enemy squadron ({fore.cyan}a{fore.white})')

    action = input()

    while action != 'm' and action != 'a':
        action = input()

    print(f'From what position would you like to {'move' if action == 'm' else 'attack'}?')

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

    if action == 'm':
        squadron = squadron_classes[board.positions[origin_coordinates[0]][origin_coordinates[1]]]
        coordinates_in_range = get_coordinates_in_range(board, origin_coordinates, squadron.move_range)

        board.print(coordinates_in_range)

        print(f'To what position in the specified range would you like to move?')

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

        move_squadron(board, origin_coordinates, next_coordinates)

        board.print([])

        print(f'{fore.green}{style.bold}{squadron.name}{style.none}{fore.white} squadron has moved: {fore.blue}{style.bold}{origin_display} - {next_display}{style.none}{fore.white}')

    if action == 'a':
        squadron = squadron_classes[board.positions[origin_coordinates[0]][origin_coordinates[1]]]
        coordinates_in_range = get_coordinates_in_range(board, origin_coordinates, squadron.attack_range)

        board.print(coordinates_in_range)

        print(f'What enemy in the specified range would you like to attack?')

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

        enemy_squadron = squadron_classes[board.positions[next_coordinates[0]][next_coordinates[1]]]
        bonus = False

        if enemy_squadron.name in squadron.bonus_against:
            bonus = True

        attack_squadron(board, squadron, next_coordinates, bonus)

    battle_user_turn(board)


def battle(user_squadrons, enemy_configuration):
    # Generate an empty board
    board = Board(
        [['-' for _ in range(board_width)] for _ in range(board_width)],
        [['-' for _ in range(board_width)] for _ in range(board_width)],
        [['-' for _ in range(board_width)] for _ in range(board_width)],
        board_height,
        board_width
    )

    board.positions[0][0] = 'A'
    board.healths[0][0] = '100'
    board.army[0][0] = 'E'

    board.print([])

    # Choose starting configuration
    for key in user_squadrons:
        for i in range(user_squadrons[key]):
            print(f'Choose a position for {style.bold}{fore.green}{squadron_classes[key].name}{style.none}{fore.white} #{i + 1}.')
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

            print(f'Imported {style.bold}{fore.green}{squadron_classes[key].name}{style.none}{fore.white} #{i + 1} at {style.bold}{fore.blue}{display}{style.none}{fore.white}.')

    # Battle!
    battle_user_turn(board)


main()