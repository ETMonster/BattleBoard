from text import *
from main import *
import string

# boards are 9x9 lists of strings of squadron types and healths
# UA = User archer squadron. EA = Enemy archer squadron. - = nothing

class Board:
    def __init__(self, positions, healths, army, height, width):
        self.positions = positions
        self.healths = healths
        self.army = army
        self.height = height
        self.width = width

    def print_board(self, board):
        print(' ', end='')
        for c in list(string.ascii_uppercase)[:self.width]:
            print(f"  {style.bold}{fore.blue}{c}{'  ' if board == self.healths else ''}", end='')

        print('')

        for i in range(self.height):
            print(f'{style.bold}{fore.blue}{i + 1}', end='')
            for j in range(self.width):
                a = self.army[i][j]
                print(f'  {style.none}{fore.green if a == 'U' else fore.red if a == 'E' else fore.white}{board[i][j]}'
                      f'{''.join([' ' for i in range(0, len(board[i][j]), -1)])}', end='')

            print('')

        print('')

    def print(self):
        print(f'{style.bold}{fore.white}POSITION BOARD')
        self.print_board(self.positions)

        print(f'{style.bold}{fore.white}HEALTH BOARD')
        self.print_board(self.healths)



Board([['E', 'X', 'U', 'X', 'E', 'U', 'X', 'E', 'U'],
['X', 'U', 'E', 'U', 'X', 'E', 'E', 'U', 'X'],
['U', 'E', 'X', 'U', 'U', 'X', 'E', 'X', 'E'],
['E', 'U', 'U', 'E', 'X', 'X', 'U', 'E', 'U'],
['X', 'E', 'U', 'X', 'U', 'X', 'E', 'E', 'U'],
['U', 'X', 'E', 'E', 'U', 'X', 'U', 'E', 'X'],
['E', 'U', 'X', 'U', 'X', 'E', 'U', 'U', 'X'],
['X', 'E', 'U', 'E', 'U', 'X', 'E', 'X', 'E'],
['U', 'X', 'X', 'E', 'U', 'E', 'U', 'X', 'U']], [['245', '783', '92', '503', '607', '155', '874', '229', '468'],
['948', '218', '340', '777', '312', '435', '564', '92', '568'],
['603', '440', '991', '564', '156', '72', '323', '891', '682'],
['789', '203', '412', '114', '852', '364', '771', '624', '45'],
['15', '784', '205', '811', '918', '233', '647', '399', '302'],
['461', '327', '57', '762', '193', '249', '304', '672', '185'],
['918', '534', '405', '982', '798', '194', '37', '267', '445'],
['180', '641', '15', '875', '324', '423', '28', '652', '806'],
['267', '754', '890', '195', '31', '450', '777', '882', '660']], [['E', 'X', 'U', 'X', 'E', 'U', 'X', 'E', 'U'],
['X', 'U', 'E', 'U', 'X', 'E', 'E', 'U', 'X'],
['U', 'E', 'X', 'U', 'U', 'X', 'E', 'X', 'E'],
['E', 'U', 'U', 'E', 'X', 'X', 'U', 'E', 'U'],
['X', 'E', 'U', 'X', 'U', 'X', 'E', 'E', 'U'],
['U', 'X', 'E', 'E', 'U', 'X', 'U', 'E', 'X'],
['E', 'U', 'X', 'U', 'X', 'E', 'U', 'U', 'X'],
['X', 'E', 'U', 'E', 'U', 'X', 'E', 'X', 'E'],
['U', 'X', 'X', 'E', 'U', 'E', 'U', 'X', 'U']], board_height, board_width).print()