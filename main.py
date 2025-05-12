import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.Font(None, 28)

# ===== Классы =====
class MenuItem:
    def __init__(self, name, base_price):
        self.name = name
        self.base_price = base_price

    def calculate_price(self):
        return self.base_price

    def display(self):
        return f"{self.name} - {self.calculate_price()}₸"

class Pizza(MenuItem):
    def __init__(self, name, base_price):
        super().__init__(name, base_price)
        self.size = None
        self.crust = None
        self.toppings = []

class Drink(MenuItem): pass
class SideDish(MenuItem): pass
class Topping(MenuItem): pass

class Button:
    def __init__(self, rect, text, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback

    def draw(self, surface):
        pygame.draw.rect(surface, (180, 180, 180), self.rect)
        pygame.draw.rect(surface, (100, 100, 100), self.rect, 2)
        text_surf = font.render(self.text, True, (0, 0, 0))
        surface.blit(text_surf, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Order:
    def __init__(self, name, type_):
        self.name = name
        self.type = type_
        self.items = []
        self.status = "Активный"

    def total(self):
        return sum(i.calculate_price() for i in self.items)

class Pizzeria:
    def __init__(self):
        self.state = "main"
        self.menu = [
            Pizza("Пицца Маргарита", 2000),
            Pizza("Пицца Пепперони", 2500),
            Drink("Coca-Cola", 500),
            Drink("Fanta", 500),
            SideDish("Картошка фри", 800),
            SideDish("Наггетсы", 1000)
        ]
        self.toppings = [Topping("Сыр", 200), Topping("Грибы", 250), Topping("Пепперони", 300)]
        self.order = []
        self.orders = []
        self.customer_name = ""
        self.selected_size = None
        self.selected_crust = None
        self.selected_toppings = []

        # Кнопки
        self.add_pizza_button = Button((50, 300, 250, 40), "Добавить пиццу", self.add_custom_pizza)
        self.confirm_button = Button((600, 500, 150, 40), "Оформить заказ", self.confirm_order)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            screen.fill((255, 255, 255))
            self.draw()
            self.handle_events()
            pygame.display.flip()
            clock.tick(30)

    def draw(self):
        if self.state == "main":
            self.draw_main_menu()
        elif self.state == "customize":
            self.draw_customize()
        elif self.state == "orders":
            self.draw_orders()

    def draw_main_menu(self):
        y = 20
        for i, item in enumerate(self.menu):
            pygame.draw.rect(screen, (230, 230, 250), (20, y, 300, 40))
            text = font.render(item.display(), True, (0, 0, 0))
            screen.blit(text, (30, y + 10))
            y += 50

        pygame.draw.rect(screen, (200, 255, 200), (350, 20, 200, 40))
        screen.blit(font.render("Настроить пиццу", True, (0, 0, 0)), (360, 30))

        self.confirm_button.draw(screen)
        pygame.draw.rect(screen, (200, 200, 255), (350, 80, 200, 40))
        screen.blit(font.render("Просмотр заказов", True, (0, 0, 0)), (360, 90))

        y = 140
        screen.blit(font.render("Корзина:", True, (0, 0, 0)), (350, y))
        y += 30
        for item in self.order:
            screen.blit(font.render(item.display(), True, (0, 0, 0)), (360, y))
            y += 25

    def draw_customize(self):
        screen.blit(font.render("Выбор размера:", True, (0, 0, 0)), (20, 20))
        sizes = ["Маленькая", "Средняя", "Большая"]
        for i, size in enumerate(sizes):
            rect = pygame.Rect(20 + i * 150, 50, 140, 40)
            pygame.draw.rect(screen, (240, 200, 200), rect)
            screen.blit(font.render(size, True, (0, 0, 0)), (rect.x + 10, rect.y + 10))

        screen.blit(font.render("Выбор теста:", True, (0, 0, 0)), (20, 110))
        crusts = ["Тонкое", "Толстое"]
        for i, crust in enumerate(crusts):
            rect = pygame.Rect(20 + i * 150, 140, 140, 40)
            pygame.draw.rect(screen, (240, 220, 200), rect)
            screen.blit(font.render(crust, True, (0, 0, 0)), (rect.x + 10, rect.y + 10))

        screen.blit(font.render("Топпинги:", True, (0, 0, 0)), (20, 200))
        for i, top in enumerate(self.toppings):
            rect = pygame.Rect(20 + i * 150, 230, 140, 40)
            pygame.draw.rect(screen, (200, 240, 200), rect)
            screen.blit(font.render(top.name, True, (0, 0, 0)), (rect.x + 10, rect.y + 10))

        self.add_pizza_button.draw(screen)

    def draw_orders(self):
        y = 20
        for i, order in enumerate(self.orders):
            screen.blit(font.render(f"{i+1}. {order.name} [{order.type}] - {order.status}", True, (0, 0, 0)), (20, y))
            y += 25
            for item in order.items:
                screen.blit(font.render(f"  - {item.display()}", True, (0, 0, 0)), (40, y))
                y += 20
            y += 10

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if self.state == "main":
                    self.handle_main_events(pos)
                elif self.state == "customize":
                    self.handle_customize_events(pos)
                elif self.state == "orders":
                    self.state = "main"

    def handle_main_events(self, pos):
        for i, item in enumerate(self.menu):
            if pygame.Rect(20, 20 + i * 50, 300, 40).collidepoint(pos):
                self.order.append(item)
        if pygame.Rect(350, 20, 200, 40).collidepoint(pos):
            self.state = "customize"
        elif self.confirm_button.is_clicked(pos):
            self.confirm_button.callback()
        elif pygame.Rect(350, 80, 200, 40).collidepoint(pos):
            self.state = "orders"

    def handle_customize_events(self, pos):
        sizes = ["Маленькая", "Средняя", "Большая"]
        for i, size in enumerate(sizes):
            if pygame.Rect(20 + i * 150, 50, 140, 40).collidepoint(pos):
                self.selected_size = size

        crusts = ["Тонкое", "Толстое"]
        for i, crust in enumerate(crusts):
            if pygame.Rect(20 + i * 150, 140, 140, 40).collidepoint(pos):
                self.selected_crust = crust

        for i, top in enumerate(self.toppings):
            if pygame.Rect(20 + i * 150, 230, 140, 40).collidepoint(pos):
                if top in self.selected_toppings:
                    self.selected_toppings.remove(top)
                else:
                    self.selected_toppings.append(top)

        if self.add_pizza_button.is_clicked(pos):
            self.add_pizza_button.callback()

    def add_custom_pizza(self):
        if self.selected_size and self.selected_crust:
            topping_names = [t.name for t in self.selected_toppings]
            name = f"Пицца ({self.selected_size}, {self.selected_crust}, {', '.join(topping_names)})"
            pizza = Pizza(name, 1500)
            if self.selected_size == "Средняя":
                pizza.base_price += 300
            elif self.selected_size == "Большая":
                pizza.base_price += 600
            pizza.toppings = self.selected_toppings.copy()
            self.order.append(pizza)
            self.selected_size = None
            self.selected_crust = None
            self.selected_toppings = []
            self.state = "main"

    def confirm_order(self):
        import tkinter as tk
        from tkinter.simpledialog import askstring
        root = tk.Tk()
        root.withdraw()
        name = askstring("Имя клиента", "Введите ваше имя:")
        if name:
            order = Order(name, "В зале")
            order.items = self.order.copy()
            self.orders.append(order)
            self.order = []

# ===== Запуск =====
if __name__ == "__main__":
    app = Pizzeria()
    app.run()
