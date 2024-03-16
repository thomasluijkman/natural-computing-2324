from math import sin, cos, atan2, radians, degrees
import random
import pygame as pg

# Parameters
N_B = 200
F_WIDTH = 1000
F_HEIGHT = 1000

class Particle:
    def __init__(self):
        self.pos = (random.randint(0,F_WIDTH), random.randint(0,F_HEIGHT))
        self
# Main function
def main():
    pg.init()  # prepare window
    pg.display.set_caption("PyNBoids")
    try: pg.display.set_icon(pg.image.load("nboids.png"))
    except: print("FYI: nboids.png icon not found, skipping..")
    # setup fullscreen or window mode
    pass

if __name__ == '__main__':
    
    main()