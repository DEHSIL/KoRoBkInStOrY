import pygame #type: ignore
import random
import sys

# --- Настройки ---
WIDTH, HEIGHT = 800, 600
FPS = 60
GHOST_LIFETIME = 700  # мс
GAME_DURATION = 30_000  # 30 секунд

# --- Инициализация ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Поймай Призрака!")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

# --- Загрузка ресурсов ---
ghost_img = pygame.image.load("img/ghost.webp")  # добавь свой ghost.png в ту же папку
ghost_img = pygame.transform.scale(ghost_img, (100, 100))
catch_sound = pygame.mixer.Sound("sound/catch.mp3")  # добавь свой catch.wav

# --- Переменные ---
score = 0
best_score = 0
start_time = 0
game_over = False
ghost_rect = ghost_img.get_rect()
ghost_visible = False
ghost_timer = 0
next_spawn_time = 0
background = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
# --- Функции ---
def spawn_ghost():
    x = random.randint(0, WIDTH - ghost_rect.width)
    y = random.randint(0, HEIGHT - ghost_rect.height)
    ghost_rect.topleft = (x, y)
    return pygame.time.get_ticks()

def draw_ui(time_left):
    score_text = font.render(f"Счёт: {score}", True, (255, 255, 255))
    time_text = font.render(f"Время: {time_left // 1000}", True, (255, 255, 255))
    tip_text = font.render("Кликай по призраку, пока не закончится время!", True, (200, 200, 200))
    screen.blit(score_text, (10, 10))
    screen.blit(time_text, (WIDTH - 150, 10))
    screen.blit(tip_text, (WIDTH // 2 - tip_text.get_width() // 2, HEIGHT - 40))

def reset_game():
    global score, start_time, game_over, ghost_visible, background, next_spawn_time
    score = 0
    start_time = pygame.time.get_ticks()
    game_over = False
    ghost_visible = False
    background = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    next_spawn_time = start_time + random.randint(1000, 2000)

# --- Старт игры ---
reset_game()

# --- Главный цикл ---
while True:
    current_time = pygame.time.get_ticks()
    time_left = GAME_DURATION - (current_time - start_time)
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if ghost_visible and ghost_rect.collidepoint(event.pos):
                score += 1
                catch_sound.play()
                ghost_visible = False  # убираем призрака после поимки

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_SPACE:
                reset_game()

    # Обновление состояния
    if not game_over:
        if current_time >= next_spawn_time and not ghost_visible:
            ghost_timer = spawn_ghost()
            ghost_visible = True

        if ghost_visible and current_time - ghost_timer > GHOST_LIFETIME:
            ghost_visible = False
            next_spawn_time = current_time + random.randint(1000, 2000)

        if time_left <= 0:
            game_over = True

    # Отрисовка
    screen.fill(background)  # черный фон

    if ghost_visible:
        screen.blit(ghost_img, ghost_rect)

    if game_over:
        best_score = score if score > best_score else best_score
        best_text = big_font.render(f"Лучший счет: {best_score}", True, (255, 0, 0))
        final_text = big_font.render(f"Время вышло! Ваш счёт: {score}", True, (255, 0, 0))
        restart_text = font.render("Нажмите ПРОБЕЛ, чтобы начать заново.", True, (255, 255, 255))
        screen.blit(final_text, (WIDTH // 2 - final_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))
        screen.blit(best_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 60))
    else:
        draw_ui(time_left)

    pygame.display.flip()
    clock.tick(FPS)
