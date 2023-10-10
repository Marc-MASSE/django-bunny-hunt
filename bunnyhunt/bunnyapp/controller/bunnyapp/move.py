import random
from bunnyapp.constants import FOREST_SIZE
from bunnyapp.models import Hunter, Rabbit, Tree, Burrow

SURROUNDING_POSITIONS = [(-1, -1), (-1, 0), (-1, +1), (0, -1), (0, +1), (+1, -1), (+1, 0), (+1, +1)]


def characters_move():
    hunter = Hunter.objects.first()
    hunter_move(hunter)
    rabbits = Rabbit.objects.all()
    for rabbit in rabbits:
        rabbit_move(rabbit)


def hunter_move(hunter):
    random.shuffle(SURROUNDING_POSITIONS)
    for dx, dy in SURROUNDING_POSITIONS:
        new_x = hunter.position_x + dx
        new_y = hunter.position_y + dy
        if (
                0 <= new_x < FOREST_SIZE
                and 0 <= new_y < FOREST_SIZE
                and not is_position_occupied(new_x, new_y)
        ):
            hunter.position_x = new_x
            hunter.position_y = new_y
            hunter.save()
            break


def rabbit_move(rabbit):
    random.shuffle(SURROUNDING_POSITIONS)
    for dx, dy in SURROUNDING_POSITIONS:
        new_x = rabbit.position_x + dx
        new_y = rabbit.position_y + dy
        if (
                0 <= new_x < FOREST_SIZE
                and 0 <= new_y < FOREST_SIZE
                and not is_position_occupied(new_x, new_y)
        ):
            rabbit.position_x = new_x
            rabbit.position_y = new_y
            rabbit.save()
            break


def is_position_occupied(x, y):
    hunter = Hunter.objects.first()
    rabbits = Rabbit.objects.all()
    trees = Tree.objects.all()
    burrows = Burrow.objects.all()

    if hunter.position_x == x and hunter.position_y == y:
        return True
    for rabbit in rabbits:
        if rabbit.position_x == x and rabbit.position_y == y:
            return True
    for tree in trees:
        if tree.position_x == x and tree.position_y == y:
            return True
    for burrow in burrows:
        if burrow.position_x == x and burrow.position_y == y:
            return True
    return False
