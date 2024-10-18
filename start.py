from text import fore, style, back
from main import start_game

print(f'{style.bold}{fore.white}Welcome to...')

print(f'{fore.white}  ____       _______ _______ _      ______        {fore.red}____         {fore.white}____   ____          _____  _____  ')
print(f'{fore.white} |  _ \\   /\\|__   __|__   __| |    |  ____|      {fore.red}/ /\\ \\       {fore.white}|  _ \\ / __ \\   /\\   |  __ \\|  __ \\ ')
print(f'{fore.white} | |_) | /  \\  | |     | |  | |    | |__        {fore.red}/ /  \\ \\      {fore.white}| |_) | |  | | /  \\  | |__) | |  | |')
print(f'{fore.white} |  _ < / /\\ \\ | |     | |  | |    |  __|      {fore.red}| |    | |     {fore.white}|  _ <| |  | |/ /\\ \\ |  _  /| |  | |')
print(f'{fore.white} | |_) / ____ \\| |     | |  | |____| |____      {fore.red}\\ \\  / /      {fore.white}| |_) | |__| / ____ \\| | \\ \\| |__| |')
print(f'{fore.white} |____/_/    \\_\\_|     |_|  |______|______|      {fore.red}\\_\\/_/       {fore.white}|____/ \\____/_/    \\_\\_|  \\_\\_____/ ')

print(f'\nPress any key to start')
x = input()

start_game()