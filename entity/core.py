import matplotlib.pyplot as plt
import time
from random import randint


class Universe:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.universe = [[0 for i in range(x)] for i in range(y)]
        self.food_count = 0
        self.entity_count = 0

class Brain:
    def __init__(self):
        self.memory = {}

    def collect_input(self):
        pass

class Entity:
    def __init__(self, x, y, genes=None, energy=50):
        self.x = x
        self.y = y
        self.energy = energy
        self.brain = Brain()
        self._genes = genes
        self._inputs = [self.look, self.listen]
        self.speak = ""

    def look(self):
        pass

    def listen(self):
        pass

    def think(self, inputs=None):
        # Read inputs
        # Do some computations: ANN goes here
        # Execute outputs
        # Example just for testing.
        actions = ['up', 'down', 'left', 'right']
        self.speak = actions[randint(0,3)]

    def reproduce(self):
        pass

    def display(self):
        return 2


class Apple:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self._color = 1

    def display(self):
        return self._color


class Gardener:
    def __init__(self, universe, quantity):
        self._universe = universe
        self._quantity = quantity
        self.garden()

    def garden(self):
        while self._universe.food_count < self._quantity:
            rand_x = randint(0, self._universe.x-1)
            rand_y = randint(0, self._universe.y-1)
            if self._universe.universe[rand_x][rand_y] == 0:
                self._universe.universe[rand_x][rand_y] = Apple(rand_x, rand_y)
                self._universe.food_count += 1


class Mover:
    def __init__(self, universe):
        self._universe = universe
        self.x_max = universe.x - 1
        self.y_max = universe.y - 1

    def up(self, x, y):
        return (x, max(0, y-1))

    def down(self, x, y):
        return (x, min(self.y_max, y+1))

    def left(self, x, y):
        return (max(0, x-1), y)

    def right(self, x, y):
        return (min(self.x_max, x+1), y)

    def move(self, entities):
        for entity in entities:
            new_x, new_y = getattr(self, entity.speak)(entity.x, entity.y)
            self._universe.universe[new_x][new_y] = entity
            self._universe.universe[entity.x][entity.y] = 0
            entity.x = new_x
            entity.y = new_y

class WorldSimulator:

    def __init__(self, x, y, food_quantity, initial_entities, iterations):
        self.universe = Universe(x, y)
        self.food_quantity = food_quantity
        self.initial_entities = initial_entities
        self.entities = []
        self.outputs = []
        self.iterations = iterations
        self.gardener = Gardener(self.universe, self.food_quantity)
        self.mover = Mover(self.universe)
        self.initialize_entities()
        self._image = None
        self.main_loop()

    def initialize_entities(self):
        while self.universe.entity_count < self.initial_entities:
            rand_x = randint(0, self.universe.x-1)
            rand_y = randint(0, self.universe.y-1)
            if self.universe.universe[rand_x][rand_y] == 0:
                entity = Entity(rand_x, rand_y)
                self.entities.append(entity)
                self.universe.universe[rand_x][rand_y] = entity
                self.universe.entity_count += 1

    def main_loop(self):
        for i in range(self.iterations):
            for entity in self.entities:
                entity.think()
            self.mover.move(self.entities)
            self.outputs = []
            self.show()
            time.sleep(0.02)

    def show(self):
        def display(item):
            if item == 0:
                return 0
            else:
                return item.display()

        image = [[display(item) for item in row] for row in self.universe.universe]

        if self._image is None:
            self._image = plt.imshow(image)
            plt.ion()
            plt.show()
        else:
            self._image.set_data(image)
            plt.draw()
            plt.pause(0.001)
