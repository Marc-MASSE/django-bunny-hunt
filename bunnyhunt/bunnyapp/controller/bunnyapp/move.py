import random
from django.core.exceptions import ObjectDoesNotExist
from bunnyapp.constants import FOREST_SIZE, DANGER_DISTANCE
from bunnyapp.models import Hunter, Rabbit, Tree, Burrow
from bunnyapp.controller.bunnyapp.trigonometry import distance, is_rabbit_hidden

# Positions one square away.
SURROUNDING_POSITIONS = [(-1, -1), (-1, 0), (-1, +1), (0, -1), (0, +1), (+1, -1), (+1, 0), (+1, +1)]
# Positions two squares away.
SURROUNDING_POSITIONS_2 = [(-2, -2), (-2, -1), (-2, 0), (-2, +1), (-2, +2), (-1, -2), (-1, +2), (0, -2), (0, +2), \
                           (+1, -2), (+1, +2), (+2, -2), (+2, -1), (+2, 0), (+2, +1), (+2, +2)]


def characters_move():
    hunter = Hunter.objects.first()
    rabbits = Rabbit.objects.all()
    burrows = Burrow.objects.all()

    # Burrow cleaning
    for burrow in burrows:
        burrow.occupied = False
        burrow.save()

    # Hunter move
    hunter.hunger += 1
    hunter_move(hunter)

    # Rabbits move
    for rabbit in rabbits:
        rabbit_move(rabbit, hunter)

    # Hunter shoot
    rabbit_hunted = hunter.hunt()
    if rabbit_hunted is not None:
        hunter.bullet -= 1
        hunter.message = f"a tiré sur le lapin ({rabbit_hunted.position_x}, {rabbit_hunted.position_y})"
        # When the hunter kills a rabbit, his hunger drops to -1.
        if is_rabbit_in_burrow(rabbit_hunted) is None:
            # Second chance to escape
            rabbit_flee(rabbit_hunted, hunter)
            rabbit_hunted = hunter.hunt()
            if rabbit_hunted is not None and is_rabbit_in_burrow(rabbit_hunted) is None:
                hunter.hunger = -1
                hunter.message = f"a tué le lapin ({rabbit_hunted.position_x}, {rabbit_hunted.position_y})"
        hunter.save()


def hunter_move(hunter):
    """
    If the hunter sees a rabbit the hunter_pursue movement is triggered.
    Otherwise, the hunter_random_move movement is triggered.
    :param hunter:
    :return: Nothing.
    """
    if closest_visible_rabbit() is not None:
        hunter_pursue(hunter, closest_visible_rabbit())
    else:
        hunter_random_move(hunter)


def hunter_random_move(hunter):
    """
    The hunter moves to a random adjacent position.
    :param hunter:
    :return: Nothing. The hunter position is updated.
    """
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
            hunter.kilometers += 1
            hunter.save()
            break


def hunter_pursue(hunter, rabbit):
    """
    The hunter moves to the adjacent position closest to the rabbit.
    :param hunter:
    :param rabbit:
    :return: Nothing. The hunter position is updated.
    """
    mini_distance = FOREST_SIZE * 2
    new_x = hunter.position_x
    new_y = hunter.position_y
    for dx, dy in SURROUNDING_POSITIONS:
        temporary_x = hunter.position_x + dx
        temporary_y = hunter.position_y + dy
        if (
                0 <= temporary_x < FOREST_SIZE
                and 0 <= temporary_y < FOREST_SIZE
                and not is_position_occupied(temporary_x, temporary_y)
        ):
            rabbit_distance = distance(
                temporary_x, temporary_y,
                rabbit.position_x, rabbit.position_y
            )
            if rabbit_distance < mini_distance:
                mini_distance = rabbit_distance
                new_x = temporary_x
                new_y = temporary_y
    hunter.position_x = new_x
    hunter.position_y = new_y
    hunter.kilometers += 1
    hunter.save()


def rabbit_move(rabbit, hunter):
    """
    If the rabbit is too close to the hunter the rabbit_pursued movement is triggered.
    Otherwise, the rabbit_random_move movement is triggered.
    :param rabbit:
    :param hunter:
    :return: Nothing
    """
    if rabbit.pursued():
        protected_place = close_to_burrow(rabbit)
        if protected_place is not None:
            rabbit.message = "se cache"
            rabbit_run_to_burrow(rabbit, protected_place)
        else:
            rabbit.message = "s'enfuit"
            rabbit_flee(rabbit, hunter)
    else:
        rabbit.message = "se promène"
        rabbit_random_move(rabbit, hunter)
        if rabbit.pursued():
            rabbit_flee(rabbit, hunter)


def rabbit_random_move(rabbit, hunter):
    """
    The rabbit moves to a random adjacent position but without being too close to the hunter.
    :param rabbit:
    :param hunter:
    :return: Nothing. The rabbit position is updated.
    """
    random.shuffle(SURROUNDING_POSITIONS)
    for dx, dy in SURROUNDING_POSITIONS:
        new_x = rabbit.position_x + dx
        new_y = rabbit.position_y + dy
        if (
                0 <= new_x < FOREST_SIZE
                and 0 <= new_y < FOREST_SIZE
                and not is_position_occupied(new_x, new_y)
                and distance(new_x, new_y, hunter.position_x, hunter.position_y) > DANGER_DISTANCE
        ):
            rabbit.position_x = new_x
            rabbit.position_y = new_y
            rabbit.kilometers += 1
            rabbit.save()
            break


def rabbit_run_to_burrow(rabbit, burrow):
    rabbit.position_x = burrow.position_x
    rabbit.position_y = burrow.position_y
    rabbit.save()
    burrow.occupied = True
    burrow.save()


def rabbit_flee(rabbit, hunter):
    """
    The rabbit flees to the adjacent position farthest from the hunter.
    :param rabbit:
    :param hunter:
    :return: Nothing. The rabbit position is updated.
    """
    max_distance = 0
    new_x = rabbit.position_x
    new_y = rabbit.position_y

    if rabbit.speed == 1:
        positions = SURROUNDING_POSITIONS
        rabbit.kilometers += 1
    else:
        positions = SURROUNDING_POSITIONS_2
        rabbit.kilometers += 2

    for dx, dy in positions:
        temporary_x = rabbit.position_x + dx
        temporary_y = rabbit.position_y + dy
        if (
                0 <= temporary_x < FOREST_SIZE
                and 0 <= temporary_y < FOREST_SIZE
                and not is_position_occupied(temporary_x, temporary_y)
        ):
            hunter_distance = distance(
                temporary_x, temporary_y,
                hunter.position_x, hunter.position_y
            )
            if hunter_distance > max_distance:
                max_distance = hunter_distance
                new_x = temporary_x
                new_y = temporary_y
    rabbit.position_x = new_x
    rabbit.position_y = new_y
    rabbit.save()


def is_position_occupied(x, y):
    """
    To check if position x,y is already occupied by an object (hunter, rabbit, tree or burrow).
    :param x:
    :param y:
    :return: True if position x,y is already occupied by an object. False otherwise.
    """
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


def closest_visible_rabbit():
    """
    To find, among the rabbits visible to the hunter, the one closest to him.
    :return: The closest rabbit if there is one. None otherwise
    """
    hunter = Hunter.objects.first()
    rabbits = Rabbit.objects.all()
    trees = Tree.objects.all()
    closest_distance = FOREST_SIZE * 2
    resulting_rabbit = None

    for rabbit in rabbits:
        if not is_rabbit_in_burrow(rabbit):
            for tree in trees:
                if not is_rabbit_hidden(
                        hunter.position_x, hunter.position_y,
                        rabbit.position_x, rabbit.position_y,
                        tree.position_x, tree.position_y
                ):
                    rabbit_distance = distance(
                        hunter.position_x, hunter.position_y,
                        rabbit.position_x, rabbit.position_y
                    )
                    if rabbit_distance < closest_distance:
                        closest_distance = rabbit_distance
                        resulting_rabbit = rabbit
                else:
                    break
    return resulting_rabbit


def is_rabbit_in_burrow(rabbit):
    """
    To check if the rabbit is at the same x,y coordinates as a burrow.
    :param rabbit:
    :return: The burrow if the rabbit is in a burrow, None otherwise.
    """
    try:
        occupied_burrow = Burrow.objects.get(position_x=rabbit.position_x, position_y=rabbit.position_y)
        return occupied_burrow
    except ObjectDoesNotExist:
        return None


def close_to_burrow(rabbit):
    """
    To check if the rabbit is close to a burrow
    :param rabbit:
    :return: The burrow if it exists, None otherwise.
    """
    burrows = Burrow.objects.all()
    for burrow in burrows:
        if distance(rabbit.position_x, rabbit.position_y, burrow.position_x, burrow.position_y) < 3\
                and not burrow.occupied:
            return burrow
    return None
