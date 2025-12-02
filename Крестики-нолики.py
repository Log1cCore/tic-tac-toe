import os
import random

STATS_DIR = "stats"
STATS_FILE = os.path.join(STATS_DIR, "results.txt")

if not os.path.exists(STATS_DIR):
    os.mkdir(STATS_DIR)

if not os.path.exists(STATS_FILE):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        f.write("human_wins: 0\nbot_wins: 0\ndraws: 0\n")

def load_stats():
    stats = {"human_wins": 0, "bot_wins": 0, "draws": 0}

    with open(STATS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                key, value = line.strip().split(": ")
                stats[key] = int(value)

    return stats

def save_stats(stats):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        f.write(f"human_wins: {stats['human_wins']}\n")
        f.write(f"bot_wins: {stats['bot_wins']}\n")
        f.write(f"draws: {stats['draws']}\n")

def update_result(result_type):
    stats = load_stats()
    if result_type == "human":
        stats["human_wins"] += 1
    elif result_type == "bot":
        stats["bot_wins"] += 1
    elif result_type == "draw":
        stats["draws"] += 1
    save_stats(stats)


def create_board(size):
    return {f"{(i-1)//size + 1}{(i-1)%size + 1}": '.' for i in range(1, size*size + 1)}

def print_board(board, size):
    count = [str(i) for i in range(1, size + 1)]
    print('  ' + ' '.join(count))
    for r in range(1, size + 1):
        row = []
        for c in range(1, size + 1):
            row.append(board[f"{r}{c}"])
        print(str(r) + ' ' + ' '.join(row))

def get_winning_lines(size):
    lines = []
    for r in range(1, size + 1):
        lines.append([f"{r}{c}" for c in range(1, size + 1)])
    for c in range(1, size + 1):
        lines.append([f"{r}{c}" for r in range(1, size + 1)])
    lines.append([f"{i}{i}" for i in range(1, size + 1)])
    lines.append([f"{i}{size - i + 1}" for i in range(1, size + 1)])
    return lines

def check_winner(board, size):
    for line in get_winning_lines(size):
        symbols = [board[pos] for pos in line]
        if symbols[0] != '.' and all(s == symbols[0] for s in symbols):
            return symbols[0]
    return None

def get_bot_move(board):
    empty_cells = [pos for pos, val in board.items() if val == '.']
    return random.choice(empty_cells) if empty_cells else None

def play_game(size, mode):
    board = create_board(size)
    if mode == 'bot':
        player_name = input('Введите ваше имя: ')
        if random.choice([True, False]):
            human_symbol = 'X'
            bot_symbol = 'O'
            print(f"{player_name} играет крестиками (X) и ходит первым.")
        else:
            human_symbol = 'O'
            bot_symbol = 'X'
            print(f"{player_name} играет ноликами (O). Бот ходит первым.")
        current_turn = 'X'
    else:
        player1 = input('Имя первого игрока: ')
        player2 = input('Имя второго игрока: ')
        players_list = [player1, player2]
        random.shuffle(players_list)
        players = {'X': players_list[0], 'O': players_list[1]}
        current_turn = 'X'
        print(f"{players['X']} играет крестиками (X) и ходит первым!")

    while True:
        print_board(board, size)

        if mode == 'bot':
            if current_turn == human_symbol:
                while True:
                    place = input(f"Ваш ход (например, 12): ").strip()
                    if place in board and board[place] == '.':
                        board[place] = human_symbol
                        break
                    else:
                        print("Неверный ход. Попробуйте снова.")
            else:
                print("Бот делает ход...")
                bot_choice = get_bot_move(board)
                board[bot_choice] = bot_symbol
                print(f"Бот пошёл на {bot_choice}")
        else:
            current_player = players[current_turn]
            while True:
                place = input(f"{current_player}, ваш ход (например, 12): ").strip()
                if place in board and board[place] == '.':
                    board[place] = current_turn
                    break
                else:
                    print("Неверный ход. Попробуйте снова.")

        winner = check_winner(board, size)
        if winner:
            print_board(board, size)
            if mode == 'bot':
                if winner == human_symbol:
                    print("Вы победили!")
                    update_result("human")
                else:
                    print("Бот победил!")
                    update_result("bot")
            else:
                winner_name = players[winner]
                print(f"{winner_name} победил!")
                update_result("human")

        if '.' not in board.values():
            print_board(board, size)
            print("Ничья!")
            update_result("draw")
            return

        current_turn = 'O' if current_turn == 'X' else 'X'


if __name__ == "__main__":
    while True:
        try:
            size = int(input('Введите размер поля (3-9): '))
            if 3 <= size <= 9:
                break
            else:
                print("Размер должен быть от 3 до 9.")
        except ValueError:
            print("Введите число!")

    while True:
        print("\nВыберите режим:")
        print("1. Против бота")
        print("2. Два игрока")
        print("0. Выход")
        choice = input("Ваш выбор: ").strip()

        if choice == '1':
            play_game(size, 'bot')
        elif choice == '2':
            play_game(size, 'human')
        elif choice == '0':
            break
        else:
            print("Неверный выбор.")

    stats = load_stats()
    total = stats['human_wins'] + stats['bot_wins'] + stats['draws']
    print(f"\nИТОГОВАЯ СТАТИСТИКА:")
    print(f"Побед человека (в одиночной игре): {stats['human_wins']}")
    print(f"Побед бота: {stats['bot_wins']}")
    print(f"Ничьих: {stats['draws']}")
    print(f"Всего сыграно игр: {total}")
    print("\nСпасибо за игру!")