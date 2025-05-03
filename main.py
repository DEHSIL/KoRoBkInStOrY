import pygame  # type: ignore
import random
import sys

# Инициализация Pygame
pygame.init()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Камень Ножницы Бумага!")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 100, 255)

win_sound = pygame.mixer.Sound('sound/win.mp3')
draw_sound = pygame.mixer.Sound('sound/draw.mp3')
lose_sound = pygame.mixer.Sound('sound/lose.mp3')

imgs = {
    'Камень': pygame.transform.scale(pygame.image.load("img/rock.png").convert(), (100, 100)),
    'Ножницы': pygame.transform.scale( pygame.image.load("img/s.png").convert(), (180, 100)),
    'Бумага': pygame.transform.scale( pygame.image.load("img/paper.png").convert(), (170, 100)),
}

# Игровые переменные
options = ['Камень', 'Бумага', 'Ножницы']
user_choice = None
computer_choice = None
result = ""
game_active = True
player_win_count = 0
computer_win_count = 0

# Прямоугольники кнопок
rock_button = pygame.Rect(100, 200, 150, 50)
paper_button = pygame.Rect(250, 200, 150, 50)
scissors_button = pygame.Rect(400, 200, 150, 50)

def draw_icon(player, computer):
    screen.blit(imgs[player], (160,80))
    screen.blit(imgs[computer], (350,80))

def draw_text(text, x, y, center=True):
    render = font.render(text, True, BLACK)
    rect = render.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(render, rect)

def get_result(user_choice, computer_choice, player_win_count, computer_win_count):
    if user_choice == computer_choice:
        draw_sound.play()
        return "Ничья!", player_win_count, computer_win_count
    elif (user_choice == "Камень" and computer_choice == "Ножницы") or \
         (user_choice == "Ножницы" and computer_choice == "Бумага") or \
         (user_choice == "Бумага" and computer_choice == "Камень"):
        win_sound.play()
        player_win_count += 1
        return "Вы выиграли!", player_win_count, computer_win_count
    else:
        lose_sound.play()
        computer_win_count += 1
        return "Вы проиграли!", player_win_count, computer_win_count

# Основной игровой цикл
running = True
while running:
    screen.fill(WHITE)
    draw_text("Камень Ножницы Бумага!", WIDTH // 2, 50)
    
    # Рисуем кнопки
    pygame.draw.rect(screen, GRAY, rock_button)
    pygame.draw.rect(screen, GRAY, paper_button)
    pygame.draw.rect(screen, GRAY, scissors_button)
    
    draw_text("Камень (R)", rock_button.centerx, rock_button.centery)
    draw_text("Бумага (P)", paper_button.centerx, paper_button.centery)
    draw_text("Ножницы (S)", scissors_button.centerx, scissors_button.centery)
    
    if game_active:
        draw_text(f"Вы: {player_win_count}  Комп: {computer_win_count}", WIDTH // 2, 450)
        draw_text("Выберите свой ход (R, P, S или нажмите кнопку)", WIDTH // 2, 120)
    else:
        draw_icon(user_choice, computer_choice)
        draw_text(f"Вы: {player_win_count}  Комп: {computer_win_count}", WIDTH // 2, 450)
        draw_text(f"Вы выбрали: {user_choice}", WIDTH // 2, 280)
        draw_text(f"Компьютер выбрал: {computer_choice}", WIDTH // 2, 320)
        draw_text(result, WIDTH // 2, 360)
        draw_text("Нажмите ПРОБЕЛ чтобы сыграть снова", WIDTH // 2, 400)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN and game_active:
            if event.key == pygame.K_r:
                user_choice = "Камень"
            elif event.key == pygame.K_p:
                user_choice = "Бумага"
            elif event.key == pygame.K_s:
                user_choice = "Ножницы"
            
            if user_choice:
                computer_choice = random.choice(options)
                result, player_win_count, computer_win_count = get_result(user_choice, computer_choice, player_win_count, computer_win_count)
                game_active = False

        elif event.type == pygame.KEYDOWN and not game_active:
            if event.key == pygame.K_SPACE:
                user_choice = None
                computer_choice = None
                result = ""
                game_active = True

        elif event.type == pygame.MOUSEBUTTONDOWN and game_active:
            if event.button == 1:
                mouse_pos = event.pos
                if rock_button.collidepoint(mouse_pos):
                    user_choice = "Камень"
                elif paper_button.collidepoint(mouse_pos):
                    user_choice = "Бумага"
                elif scissors_button.collidepoint(mouse_pos):
                    user_choice = "Ножницы"

                if user_choice:
                    computer_choice = random.choice(options)
                    result, player_win_count, computer_win_count = get_result(user_choice, computer_choice, player_win_count, computer_win_count)
                    game_active = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
