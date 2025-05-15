import pygame #type: ignore 
import random

pygame.init()
WIDTH = HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Traffic Lights")
clock = pygame.time.Clock()

BLACK = (10, 10, 10)
WHITE = (240, 240, 240)
GREEN = (50, 255, 100)
RED = (255, 60, 60)
YELLOW = (255, 215, 0)
GRAY = (50, 50, 50)
NEON_BLUE = (0, 255, 255)
NEON_PURPLE = (180, 0, 255)

FONT = pygame.font.SysFont("consolas", 24)

traffic_light_ns = "greeen"
traffic_light_ew = "red"
auto_mode = False
last_switch_time = 0
SWITCH_INTERVAL = 4000

cars = []
passed_cars = 0



def draw_buttons(text, x, y, w, h, hovered):
    color = NEON_PURPLE if hovered else NEON_BLUE
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
    pygame.draw.rect(screen, WHITE, (x, y, w, h), 2, border_radius=10)
    label = FONT.render(text, True, (WHITE if hovered else BLACK))
    screen.blit(label, (x+w//2 - label.get_width()//2, y+h//2 - label.get_height()//2))
    return pygame.Rect(x, y, w, h)


def draw_interseption():
    screen.fill(BLACK)

    pygame.draw.rect(screen, GRAY, (300, 0, 200, HEIGHT))
    pygame.draw.rect(screen, GRAY, (0, 300, WIDTH, 200))

    for i in range(0, WIDTH, 40):
        pygame.draw.line(screen, WHITE, (i, 395), (i+20, 395), 2)
    for i in range(0, HEIGHT, 40):
        pygame.draw.line(screen, WHITE, (395, i), (395, i+20), 2)


def draw_traffic_lights():
    color_ns = GREEN if traffic_light_ns == "green" else RED
    pygame.draw.circle(screen, color_ns, (300, 250), 15)

    color_ns2 = GREEN if traffic_light_ns == "green" else RED
    pygame.draw.circle(screen, color_ns2, (500, 550), 15)

    color_ew = GREEN if traffic_light_ew == "green" else RED
    pygame.draw.circle(screen, color_ew, (550, 300), 15)

    color_ew2 = GREEN if traffic_light_ew == "green" else RED
    pygame.draw.circle(screen, color_ew2, (260, 500), 15)

def draw_cars():
    for car in cars:
        pygame.draw.rect(screen, (random.randint(100,255), random.randint(100,255), random.randint(100,255)),
                         (car[0], car[1], 20, 10)) 
        

def update_cars():
    global passed_cars
    for car in cars:
        x, y, dx, dy = car
     
        if dx > 0 and x < 220 or dx < 0 and x > 580 or dy > 0 and y < 220 or dy < 0 and y > 580:
            car[0] += dx
            car[1] += dy
        elif dy == 2:
            if traffic_light_ns == "green" or y > 220:
                car[1] += dy
        elif dy == -2:
            if traffic_light_ns == "green" or  y < 580:
                car[1] += dy
        elif dx == 2:
            if traffic_light_ew == "green" or  x > 22:
                car[0] += dx 
        elif dx == -2:
            if traffic_light_ew == "green" or  x < 58:
                car[0] += dx

    for car in cars[:]:
        if not (0 <= car[0] <= WIDTH and 0 <= car[1] <= HEIGHT):
            cars.remove(car)
            passed_cars += 1


def spawn_car():
    direction = random.choice(['N', 'S', 'E', 'W'])
    if direction == 'N':
        cars.append([345, 0, 0, 2])
    elif direction == 'S':
        cars.append([445, HEIGHT, 0, -2])
    elif direction == 'E':
        cars.append([0, 445, 2, 0])
    elif direction == 'W':
        cars.append([WIDTH, 345, -2, 0])    


def toggle_lights():
    global traffic_light_ns, traffic_light_ew
    traffic_light_ns = "green" if traffic_light_ns == "red" else "red"
    traffic_light_ew = "green" if traffic_light_ew == "red" else "red"


def auto_switch():
    global last_switch_time

    if pygame.time.get_ticks() - last_switch_time > SWITCH_INTERVAL:
        toggle_lights()
        last_switch_time = pygame.time.get_ticks()


def main():
    running = True
    global last_switch_time, auto_mode, cars
    while running:
        clock.tick(60)
        draw_interseption()
        draw_traffic_lights()
        draw_cars()

        if random.randint(0, 60) < 2:
            spawn_car()

        update_cars()
        mouse = pygame.mouse.get_pos()
        manual_btn = draw_buttons("Переключить вручную", 30, 700, 250, 50, pygame.Rect(50, 700, 250, 50).collidepoint(mouse))
        auto_btn = draw_buttons("Авто режим: " + ("ВКЛ" if auto_mode else "ВЫКЛ"), 525, 700, 250, 50, pygame.Rect(500, 700, 250, 50).collidepoint(mouse))
        
        count_label = FONT.render(f"Проехало машин: {passed_cars}", True, NEON_BLUE)
        screen.blit(count_label, (WIDTH//2 - count_label.get_width()//2, 20))

        if auto_mode:
            auto_switch()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if manual_btn.collidepoint(event.pos):
                    toggle_lights()
                elif auto_btn.collidepoint(event.pos):
                    auto_mode = not auto_mode
                    last_switch_time = pygame.time.get_ticks()

    pygame.quit()

if __name__ == "__main__":
    main()
