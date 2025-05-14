import pygame # type: ignore
import random

pygame.init()
WIDTH, HEIGHT = 800, 600 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Parking")

FONT = pygame.font.SysFont("Arial", 20)

GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SLOT_COUNT = 20
SLOT_SIZE = 30
SLOT_MARGIN = 5
parking_slots = [None] * SLOT_COUNT

buttons = {
    "in": pygame.Rect(600, 100, 180, 40),
    "out": pygame.Rect(600, 160, 180, 40),
}

current_car = None

car_types = {
    "легковая": {"size": 1, "color": (255,0,0)},
    "грузовая": {"size": 2, "color": (0,0,255)},
    "электромобиль": {"size": 1, "color": (0,255,0)},
}


def generate_car():
    plate = f"{random.choice('QAZWXSECDRV')}{random.randint(100,999)}{random.choice("QAZWXSEDCRFV")}"
    car_type = random.choice(list(car_types.keys()))
    car = {
        "plate": plate,
        "type": car_type,
        "size": car_types[car_type]["size"],
        "color": car_types[car_type]["color"]
    }
    return car


def draw_parking(surface, slots):
    x, y = 20, 20
    for i, slot in enumerate(slots):
        rect = pygame.Rect(x, y, SLOT_SIZE, SLOT_SIZE)
        color = RED if slot else GREEN
        pygame.draw.rect(surface, color, rect)
        x += SLOT_SIZE + SLOT_MARGIN

        if (i + 1 ) % 10 == 0:
            x = 20
            y+= SLOT_SIZE + SLOT_MARGIN


def park_car(car):
    for i in range(SLOT_COUNT - car["size"] + 1 ):
        if all(parking_slots[i + j] is None for j in range(car["size"])):  
            for j in range(car["size"]):
                parking_slots[i + j] = car
            return True 
    return False       


def remove_random_car():
    indices = [i for i, slot in enumerate(parking_slots) if slot is not None]
    if not indices:
        return "Парковка пуста"
    index = random.choice(indices)
    car = parking_slots[index]
    for i in range(SLOT_COUNT):
        if parking_slots[i] == car:
            parking_slots[i] = None
    return f"Машине {car["plate"]} Покинула парковку"   
     

def draw_ui():
    pygame.draw.rect(WIN, GRAY, buttons["in"])
    pygame.draw.rect(WIN, GRAY, buttons["out"])
    WIN.blit(FONT.render("Впустить машину", True, BLACK), (610, 110))
    WIN.blit(FONT.render("Выпустить машину", True, BLACK), (610, 170))

    occupied = sum(1 for slot in parking_slots if slot)
    WIN.blit(FONT.render(f"Занято: {occupied}", True, BLACK), (600, 250))
    WIN.blit(FONT.render(f"Свободно: {SLOT_COUNT - occupied}", True, BLACK), (600, 280))

    if current_car:
        WIN.blit(FONT.render(f"Машина на въезде", True, BLACK), (600, 320))
        WIN.blit(FONT.render(f"Номер: {current_car["plate"]}", True, BLACK), (600, 350))
        WIN.blit(FONT.render(f"Тип: {current_car["type"]}", True, current_car['color']), (600, 380))


def handler_click(pos):
    global current_car
    if buttons["in"].collidepoint(pos):
        if not current_car:
            current_car = generate_car()
        else:
            if park_car(current_car):
                current_car = None
            else:
                print("нет мест")
    elif buttons["out"].collidepoint(pos):
        message = remove_random_car()
        print(message)   

def main():
    global current_car
    clock = pygame.time.Clock()
    run = True
    while run:
        WIN.fill(WHITE)
        draw_parking(WIN, parking_slots)
        draw_ui()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handler_click(event.pos)

        clock.tick(30)

    pygame.quit()
    
if __name__ == "__main__":
    main()    