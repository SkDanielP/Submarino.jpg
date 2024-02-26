import pygame

import sys

from pygame.locals import *

# -----------
cooldown_time = 1000

# Constants

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
missile_image_pos_yLim = 600

submarine_image_pos_y_init = sea_level

submarine_image_pos_x_init = 10

# Gravity constant

g = 9.8

# Fluid density  1000 m^3/kg for water

p = 1000

# Robot total volume

v = 1

# Delta time. It depends on CPU clock frequency and computational complexity

dt = 0.001

# Friction constant

b_y = 5000

b_x = 500

# Buoyancy

e = - (p * g * v)

# Force in x

force = 100

# Tank variables

actual_level = 1000
valve_flow = 10
max_capacity = 2000
fluid_to_pump = 'air'

# Submarine variables

mass = 2
actual_velocity_x = float(0)
actual_velocity_y = 0

# missile variable

mass_missile = 1010
throwing_force = 500
vel_x = 0
vel_y = 0
is_shooted = False
b_missile = 100


# ------------------------------

# Classes and Functions

# ------------------------------


class Reservoir:

    def __init__(self, actual_level, valve_flow, max_capacity, fluid_to_pump):

        self.actual_level = actual_level

        self.valve_flow = valve_flow

        self.max_capacity = max_capacity

        self.fluid_to_pump = fluid_to_pump

    def pumping_air_water(self, fluid_to_pump):

        if fluid_to_pump == 'air':

            if self.actual_level > 0:

                self.actual_level = self.actual_level - self.valve_flow

            else:

                self.actual_level = 0

        if fluid_to_pump == 'water':

            if self.actual_level < self.max_capacity:

                self.actual_level = self.actual_level + self.valve_flow

            else:

                self.actual_level = self.max_capacity


class Missile:
    def __init__(self, vel_x, vel_y, throwing_force, mass_missile, is_shooted):

        self.vel_y = vel_x

        self.vel_x = vel_y

        self.throwing_force = throwing_force

        self.mass_missile = mass_missile

        self.is_shooted = is_shooted

        self.pos_x = 0

        self.pos_y = 0

        self.is_stopped = True

        self.direction = 'right'

    def set_position(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def set_velocity(self, vel_x, vel_y):
        self.vel_x = vel_x
        self.vel_y = vel_y

    def calculate_velocity(self):
        # Calculate the velocity in x
        self.vel_x = dt * ((self.throwing_force / self.mass_missile) - (
                (b_missile * self.vel_x) / self.mass_missile)) + self.vel_x

        # Calculate the velocity in y
        self.vel_y = dt * (
                (e / self.mass_missile) + g - ((b_missile * self.vel_y) / self.mass_missile)) + self.vel_y

    def calculate_position(self):
        # Calculate the new position in x
        self.pos_x = self.pos_x + self.vel_x
        if self.pos_x <= screen_left_limit:
            self.pos_x = screen_right_limit
        # Calculate the new position in y
        self.pos_y = self.pos_y + self.vel_y
        if self.pos_y >= missile_image_pos_yLim:
            self.pos_y = missile_image_pos_yLim
        elif self.pos_y <= sea_level:
            self.pos_y = sea_level

    def is_missile_on_limit(self):
        if (self.pos_x >= screen_right_limit or
                self.pos_x <= screen_left_limit or
                self.pos_y >= missile_image_pos_yLim or
                self.pos_y <= sea_level):
            return True
        return False


class Engine:
    def __init__(self):
        self.force = 0

    def accelerate(self, force):
        self.force = force

    def brake(self):
        self.force = 0


class Submarine:

    def __init__(self, tank, mass, actual_velocity_x, actual_velocity_y, pos_x, pos_y, engine, missile):

        self.pos_x = pos_x

        self.pos_y = pos_y

        self.mass = mass

        self.actual_velocity_x = actual_velocity_x

        self.actual_velocity_y = actual_velocity_y

        self.tank = tank

        self.engine = engine

        self.missile = missile

        self.last_shot_time = 0

    def calculate_mass(self):

        self.mass = self.tank.actual_level  # + self.mass

    def calculate_velocity(self):
        # Calcular la velocidad en el eje x
        self.actual_velocity_x = dt * ((self.engine.force / self.mass) - (
                (b_x * self.actual_velocity_x) / self.mass)) + self.actual_velocity_x

        # Calcular la velocidad en el eje y
        self.actual_velocity_y = dt * (
                (e / self.mass) + g - ((b_y * self.actual_velocity_y) / self.mass)) + self.actual_velocity_y

    def calculate_position(self):
        # Calcular la nueva posición en el eje x
        self.pos_x = self.pos_x + self.actual_velocity_x
        if self.pos_x >= screen_right_limit:
            self.pos_x = screen_left_limit
        elif self.pos_x <= screen_left_limit:
            self.pos_x = screen_right_limit

        # Calcular la nueva posición en el eje y
        self.pos_y = self.pos_y + self.actual_velocity_y
        if self.pos_y >= submarine_image_pos_yLim:
            self.pos_y = submarine_image_pos_yLim
        if self.pos_y <= sea_level:
            self.pos_y = sea_level

    def launch_missile(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > cooldown_time:
            self.missile.is_shooted = True
            self.last_shot_time = current_time

    def reload_missile(self):
        self.missile.set_position(self.pos_x + 45, self.pos_y + 10)
        self.missile.set_velocity(0, 0)


# --------------------------------------------


# ------------------------------

# Main function

# ------------------------------

def define_missile_movement(submarine):
    if submarine.missile.direction == 'right':
        submarine.missile.throwing_force = throwing_force
    elif submarine.missile.direction == 'left':
        submarine.missile.throwing_force = -throwing_force


def set_static_missile(submarine):
    if submarine.missile.is_shooted:
        submarine.missile.calculate_position()
        submarine.missile.calculate_velocity()
    else:
        submarine.reload_missile()



def main():

    pygame.init()

    # define variables

    tank1 = Reservoir(actual_level, valve_flow, max_capacity, fluid_to_pump)

    engine1 = Engine()

    missile1 = Missile(vel_x, vel_y, throwing_force, mass_missile, is_shooted)

    submarine1 = Submarine(tank1, mass, actual_velocity_x, actual_velocity_y, submarine_image_pos_x_init,
                           submarine_image_pos_y_init, engine1, missile1)

    # --------------------------------------------

    # Creation of the window and assigning a title

    # --------------------------------------------

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.display.set_caption("Submarine game")

    # -----------------------------------------

    # Load images (creation of Surface objects)

    # -----------------------------------------

    background_image = pygame.image.load("mar.jpg").convert()

    # Some image formats needs alpha conversion

    submarine_image = pygame.image.load("sub.png").convert_alpha()

    missile_image = pygame.image.load("misil.png").convert_alpha()

    boom_image = pygame.image.load("boom.png").convert_alpha()

    # --------------------------------------------

    # The blit method place images onto screen

    # We specify the position of the 'Surface' on the window

    # --------------------------------------------

    screen.blit(submarine_image, (submarine_image_pos_x_init, submarine_image_pos_y_init))

    screen.blit(background_image, (0, 0))

    # --------------------------------------------

    # Displaying changes on the screen

    # --------------------------------------------

    pygame.display.flip()

    # Main loop

    while True:

        # place Images onto screen

        # --------------------------------------------

        screen.blit(background_image, (0, 0))

        screen.blit(submarine_image, (submarine1.pos_x, submarine1.pos_y))

        # logic

        submarine1.calculate_velocity()
        submarine1.calculate_position()

        if submarine1.missile.is_shooted:
            screen.blit(missile_image, (submarine1.missile.pos_x, submarine1.missile.pos_y))
            submarine1.missile.calculate_velocity()
            submarine1.missile.calculate_position()
            if submarine1.missile.is_missile_on_limit():
                submarine1.missile.is_shooted = False

        else:

            define_missile_movement(submarine1)
            set_static_missile(submarine1)

        # --------------------------------------------

        # Re-draw all elements

        # --------------------------------------------

        pygame.display.flip()

        # --------------------------------------------

        # Possible mouse and keyboard inputs

        # --------------------------------------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                sys.exit()

            elif event.type == pygame.KEYDOWN:

                if event.key == K_UP:

                    tank1.pumping_air_water('air')

                elif event.key == K_DOWN:

                    tank1.pumping_air_water('water')

                elif event.key == K_LEFT:
                    submarine1.engine.brake()
                    submarine1.engine.accelerate(-force)
                    submarine_image = pygame.image.load("sub2.png").convert_alpha()
                    if not submarine1.missile.is_shooted:
                        submarine1.missile.direction = 'left'
                        missile_image = pygame.image.load("misil2.png").convert_alpha()


                elif event.key == K_RIGHT:

                    submarine1.engine.brake()
                    submarine1.engine.accelerate(force)
                    submarine_image = pygame.image.load("sub.png").convert_alpha()
                    if not submarine1.missile.is_shooted:
                        submarine1.missile.direction = 'right'
                        missile_image = pygame.image.load("misil.png").convert_alpha()


                elif event.key == K_SPACE:
                    submarine1.engine.brake()

                elif event.key == K_x:
                    submarine1.launch_missile()

        submarine1.calculate_mass()


if __name__ == "__main__":
    main()
