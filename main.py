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

    def print_board(self, board, print_range, squadron):

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
                      f'{fore.green if a == 'U' else fore.red if a == 'E' else fore.magenta if (abs(i - squadron[0]) <= print_range and abs(j - squadron[1]) <= print_range) and print_range > 0 else fore.white}'
                      f'{board[i][j]}'
                      f'{(' ' * ((3 - len(board[i][j])) + 2)) if board == self.healths else '  '}', end='')

            print('')

        print('')

    def print(self, print_range, squadron):
        print(f'{style.bold}{fore.white}POSITION BOARD')
        self.print_board(self.positions, print_range, squadron)

        print(f'{style.bold}{fore.white}HEALTH BOARD')
        self.print_board(self.healths, print_range, squadron)

class SquadronClass:
    def __init__(self, health, attack_range, move_range, damage, bonus_damage, bonus_against):
        self.health = health
        self.attack_range = attack_range
        self.move_range = move_range
        self.damage = damage
        self.bonus_damage = bonus_damage
        self.bonus_against = bonus_against

squadron_classes = {
    'A': SquadronClass(100, 4, 1, 60, 30, ['S', 'F']),
    'F': SquadronClass(350, 1, 2, 45, 30, ['M', 'A']),
    'S': SquadronClass(650, 1, 1, 10, 100, ['C', 'F']),
    'C': SquadronClass(500, 1, 4, 50, 30, ['A', 'M']),
    'M': SquadronClass(200, 3, 2, 30, 40, ['S', 'C'])
}


def main():
    battle_squadrons = {
        'A': 1,
        'F': 0,
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

def battle_user_turn(board):
    print(f'{style.under}USER TURN{style.none}{fore.white}')
    print(f'Move a friendly squadron ({fore.cyan}m{fore.white}) OR attack an enemy squadron ({fore.cyan}a{fore.white})')

    action = input()

    while action != 'm' and action != 'a':
        action = input()

    print(f'From what position would you like to {'move' if action == 'm' else 'attack'}?')

    if action == 'm':
        origin_display = ''
        origin_coordinates = []
        origin_taken = False
        origin_is_enemy = False

        while not origin_taken or origin_is_enemy:
            origin_input = get_position_input(board)

            origin_position = origin_input[0]
            origin_coordinates = origin_input[1]
            origin_taken = origin_input[2]
            origin_is_enemy = origin_input[3]

        board.print(squadron_classes[board.positions[origin_coordinates[0]][origin_coordinates[1]]].move_range, origin_coordinates)

        print(f'To what position in the specified range would you like to move?')

    #board.print(squadron_classes[board.positions[2][2]].attack_range, [2, 2])



def battle(user_squadrons, enemy_configuration):
    # Generate an empty board
    board = Board(
        [['-' for _ in range(board_width)] for _ in range(board_width)],
        [['-' for _ in range(board_width)] for _ in range(board_width)],
        [['-' for _ in range(board_width)] for _ in range(board_width)],
        board_height,
        board_width
    )

    board.print(0, [0, 0])

    # Choose starting configuration
    for key in user_squadrons:
        for i in range(user_squadrons[key]):
            print(f'Choose a position for {style.bold}{fore.green}{key}{style.none}{fore.white} #{i + 1}.')
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
            board.print(0, [0, 0])

            print(f'Imported {style.bold}{fore.green}{key}{style.none}{fore.white} #{i + 1} at {style.bold}{fore.blue}{display}{style.none}{fore.white}.')

    # Battle!
    battle_user_turn(board)


main()