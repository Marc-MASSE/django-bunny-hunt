import math


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def hunter_blind_spot(hunter_x, hunter_y, tree_x, tree_y):
    """
    To calculate the angle where the rabbits can be hidden.
    :param hunter_x: hunter x position
    :param hunter_y: hunter y position
    :param tree_x: tree x position
    :param tree_y: tree y position
    :return: an angle
    """
    return math.atan(2 / distance(hunter_x, hunter_y, tree_x, tree_y))


def is_rabbit_hidden(hunter_x, hunter_y, rabbit_x, rabbit_y, tree_x, tree_y):
    """
    To check if a rabbit is hidden behind a tree
    :param hunter_x: hunter x position
    :param hunter_y: hunter y position
    :param rabbit_x: rabbit x position
    :param rabbit_y: rabbit y position
    :param tree_x: tree x position
    :param tree_y: tree y position
    :return: True if the rabbit is hidden. False otherwise.
    """
    # To calculate the scalar product of hunter-tree and hunter-rabbit vectors
    scalar_product = ((tree_x - hunter_x) * (rabbit_x - hunter_x)
                      + (tree_y - hunter_y) * (rabbit_y - hunter_y))

    # To calculate the angle between hunter-tree and hunter-rabbit vectors
    hunter_tree_distance = distance(hunter_x, hunter_y, tree_x, tree_y)
    hunter_rabbit_distance = distance(hunter_x, hunter_y, rabbit_x, rabbit_y)
    cosine_value = scalar_product / (hunter_tree_distance * hunter_rabbit_distance)
    cosine_value = max(-1, min(1, cosine_value))  # To avoid rounding problems in calculations
    angle_tree_hunter_rabbit = math.acos(cosine_value)

    # To check if the rabbit is hidden by the tree
    if ((abs(angle_tree_hunter_rabbit) < abs(hunter_blind_spot(hunter_x, hunter_y, tree_x, tree_y)))
            and (distance(hunter_x, hunter_y, rabbit_x, rabbit_y) > distance(hunter_x, hunter_y, tree_x, tree_y))):
        return True
    return False
