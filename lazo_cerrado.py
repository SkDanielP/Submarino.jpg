import pygame
import sys
import matplotlib.pyplot as plt

# Constantes
SCREEN_WIDTH = 1257
SCREEN_HEIGHT = 666

submarine_width = 100
submarine_height = 50

screen_left_limit = 0
screen_right_limit = SCREEN_WIDTH - submarine_width
screen_top_limit = 0
screen_bottom_limit = SCREEN_HEIGHT - submarine_height

sea_level = 80
submarine_image_pos_yLim = 550

submarine_image_pos_y_init = sea_level
submarine_image_pos_x_init = 10

g = 9.8
p = 1000
v = 1
dt = 0.01
b_y = 150
b_x = 500
e = - (p * g * v)
force = 50

# Variables del tanque
actual_level = 1000
valve_flow = 0.001
max_capacity = 1050
fluid_to_pump = 'air'

# Variables del submarino
mass = 2
actual_velocity_x = 0
actual_velocity_y = 0

target_pos = 0

# grafica
submarine_y_position = []


# Clases y funciones


class Pointer:
    is_active = False
    pos_pointed_x = 0
    pos_pointed_y = 0

    def set_position(self, x, y):
        self.pos_pointed_x = x
        self.pos_pointed_y = y

    def point(self, x, y):
        self.is_active = True
        self.set_position(x, y)

    def finish_pointing(self):
        self.is_active = False


class Reservoir:
    def __init__(self, actual_level, valve_flow, max_capacity, fluid_to_pump):
        self.actual_level = actual_level
        self.valve_flow = valve_flow
        self.max_capacity = max_capacity
        self.fluid_to_pump = fluid_to_pump

    def pumping_air_water(self, fluid_to_pump):
        if fluid_to_pump == 'air':
            self.actual_level = 995
        elif fluid_to_pump == 'water':
            self.actual_level = 1010
        else:
            self.actual_level = 1000


class Engine:
    def __init__(self):
        self.force = 0

    def accelerate(self, force):
        self.force = force

    def brake(self):
        self.force = 0


class Submarine:
    def __init__(self, tank, mass, actual_velocity_x, actual_velocity_y, pos_x, pos_y, engine):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.mass = mass
        self.actual_velocity_x = actual_velocity_x
        self.actual_velocity_y = actual_velocity_y
        self.tank = tank
        self.engine = engine
        self.pointer = Pointer()

    def calculate_mass(self):
        self.mass = self.tank.actual_level

    def calculate_velocity(self):

        self.actual_velocity_x = dt * ((self.engine.force / self.mass) - (
                (b_x * self.actual_velocity_x) / self.mass)) + self.actual_velocity_x

        self.actual_velocity_y = dt * (
                (e / self.mass) + g - ((b_y * self.actual_velocity_y) / self.mass)) + self.actual_velocity_y

    def calculate_position(self):

        self.pos_x = self.pos_x + self.actual_velocity_x
        if self.pos_x >= screen_right_limit:
            self.pos_x = screen_left_limit

        self.pos_y = self.pos_y + self.actual_velocity_y
        if self.pos_y >= submarine_image_pos_yLim:
            self.pos_y = submarine_image_pos_yLim
        if self.pos_y <= sea_level:
            self.pos_y = sea_level


# Función principal
def main():
    pygame.init()

    tank1 = Reservoir(actual_level, valve_flow, max_capacity, fluid_to_pump)
    engine1 = Engine()
    submarine1 = Submarine(tank1, mass, actual_velocity_x, actual_velocity_y, submarine_image_pos_x_init,
                           submarine_image_pos_y_init, engine1)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Submarine game")

    background_image = pygame.image.load("mar.jpg").convert()
    submarine_image = pygame.image.load("sub.png").convert_alpha()

    screen.blit(submarine_image, (submarine_image_pos_x_init, submarine_image_pos_y_init))
    screen.blit(background_image, (0, 0))
    pygame.display.flip()

    while True:

        screen.blit(background_image, (0, 0))
        screen.blit(submarine_image, (submarine1.pos_x, submarine1.pos_y))

        submarine1.calculate_velocity()
        submarine1.calculate_position()

        submarine_y_position.append(submarine1.pos_y)

        pygame.display.flip()

        if submarine1.pointer.is_active:

            if submarine1.pointer.pos_pointed_x > submarine1.pos_x:
                engine1.accelerate(force)
                submarine_image = pygame.image.load("sub.png").convert_alpha()

            elif 25 > submarine1.pointer.pos_pointed_x - submarine1.pos_x > - 25:
                engine1.brake()

            elif submarine1.pointer.pos_pointed_x < submarine1.pos_x:
                engine1.accelerate(-force)
                submarine_image = pygame.image.load("sub2.png").convert_alpha()

            if submarine1.pointer.pos_pointed_y > submarine1.pos_y:
                tank1.pumping_air_water('water')
            elif submarine1.pointer.pos_pointed_y < submarine1.pos_y:
                tank1.pumping_air_water('air')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                plt.plot(range(len(submarine_y_position)), submarine_y_position)
                plt.xlabel('T')
                plt.ylabel('Y')
                plt.title('y vs t')
                plt.show()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                submarine1.pointer.point(mouse_position[0] - 90, mouse_position[1] - 30)

        submarine1.calculate_mass()


if __name__ == "__main__":
    main()
