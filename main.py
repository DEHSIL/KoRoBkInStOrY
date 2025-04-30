import random

# Класс игрока
class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.health = 100

    def move(self, direction):
        if direction == 'w':
            self.x -= 1
        elif direction == 's':
            self.x += 1
        elif direction == 'a':
            self.y -= 1
        elif direction == 'd':
            self.y += 1

class Enemy:
    def __init__(self):
        self.x = random.randint(2,4)
        self.y = random.randint(2,4)

    def move(self, player):
        # Двигается на один шаг ближе к игроку
        if self.x < player.x:
            self.x += 1
        elif self.x > player.x:
            self.x -= 1
        elif self.y < player.y:
            self.y += 1
        elif self.y > player.y:
            self.y -= 1
        
    
# Функция генерации игрового поля
def generate_field():
    field = [['.' for _ in range(5)] for _ in range(5)]

    # Установка ловушек
    traps = random.randint(3, 5)
    placed = 0
    while placed < traps:
        x, y = random.randint(0, 4), random.randint(0, 4)
        if (x, y) != (0, 0) and field[x][y] == '.':
            field[x][y] = 'T'
            placed += 1

    # Установка выхода
    while True:
        x, y = random.randint(0, 4), random.randint(0, 4)
        if (x, y) != (0, 0) and field[x][y] == '.':
            field[x][y] = 'X'
            break

    return field

# Функция отображения поля
def print_field(field, player, enemy):
    for i in range(5):
        row = ''
        for j in range(5):
            if i == player.x and j == player.y:
                row += 'P '
            elif i == enemy.x and j == enemy.y:
                row += 'E '
            else:
                row += field[i][j] + ' '
        print(row)
    print(f"Здоровье: {player.health}\n")

# Проверка границ
def is_valid_move(x, y):
    return 0 <= x < 5 and 0 <= y < 5

# Основной игровой процесс
def play_game():
    field = generate_field()
    player = Player()
    enemy = Enemy()

    while True:
        print_field(field, player, enemy)

        move = input("Введите направление (w/a/s/d): ").strip().lower()
        if move not in ['w', 'a', 's', 'd']:
            print("Недопустимое направление!\n")
            continue

        # Проверка, не выйдет ли игрок за границы
        new_x, new_y = player.x, player.y
        if move == 'w':
            new_x -= 1
        elif move == 's':
            new_x += 1
        elif move == 'a':
            new_y -= 1
        elif move == 'd':
            new_y += 1

        if not is_valid_move(new_x, new_y):
            print("Нельзя выйти за границы поля!\n")
            continue

        player.move(move)
        current_cell = field[player.x][player.y]
        enemy.move(player)

        if current_cell == 'T':
            print("Вы наступили на ловушку! -30 здоровья!\n")
            player.health -= 30
            field[player.x][player.y] = '.'
        elif player.x == enemy.x and player.y == enemy.y:
            print("Вы попались врагу! -100 здоровья!\n")
            player.health -= 100
        elif current_cell == 'X':
            print("Вы нашли выход! Победа!\n")
            break

        if player.health <= 0:
            print("Вы проиграли. Здоровье закончилось.\n")
            break

# Повтор игры
def main():
    while True:
        play_game()
        again = input("Хотите сыграть снова? (y/n): ").strip().lower()
        while again != 'y':
            again = input("Хотите сыграть снова? (y/n): ").strip().lower()
            if again == 'n':
             print("Спасибо за игру!")
             exit()

if __name__ == "__main__":
    main()
