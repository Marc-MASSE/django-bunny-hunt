import random

from django.shortcuts import render, redirect

from bunnyapp.constants import FOREST_SIZE, BULLET_NUMBER, HUNTER_POSITION_X, HUNTER_POSITION_Y, TREES_NUMBER, \
    BURROWS_NUMBER, RABBITS_NUMBER
from bunnyapp.models import Forest, Hunter, Tree, Burrow, Rabbit
from bunnyapp.controller.bunnyapp.move import characters_move


def welcome(request):
    if request.method == 'POST':
        # To delete all previous forests.
        existing_forest = Forest.objects.filter().first()
        if existing_forest:
            Tree.objects.filter(forest=existing_forest).delete()
            Burrow.objects.filter(forest=existing_forest).delete()
            Hunter.objects.filter(forest=existing_forest).delete()
            Rabbit.objects.filter(forest=existing_forest).delete()
            existing_forest.delete()

        # To initialise the forest
        forest = Forest.objects.create(size=FOREST_SIZE)
        initialize_forest(forest)
        return redirect('game')

    return render(request, 'bunnyapp/welcome.html')


def game(request):
    # To retrieve forest and its component data from the database
    forest = Forest.objects.first()

    if request.method == 'POST':
        characters_move()
        return redirect('game')

    trees = Tree.objects.filter(forest=forest)
    hunters = Hunter.objects.filter(forest=forest)
    rabbits = Rabbit.objects.filter(forest=forest)
    burrows = Burrow.objects.filter(forest=forest)

    # To create the board from this data
    board = [['' for _ in range(forest.size)] for _ in range(forest.size)]

    for tree in trees:
        board[tree.position_y][tree.position_x] = 'tree'

    for hunter in hunters:
        board[hunter.position_y][hunter.position_x] = 'hunter'

    for rabbit in rabbits:
        board[rabbit.position_y][rabbit.position_x] = 'rabbit'

    for burrow in burrows:
        board[burrow.position_y][burrow.position_x] = 'burrow'

    for burrow in burrows:
        for rabbit in rabbits:
            if rabbit.position_x == burrow.position_x and rabbit.position_y == burrow.position_y:
                board[burrow.position_y][burrow.position_x] = 'hidden'

    context = {
        'board': board,
        'forest': forest,
        'hunters': hunters,
        'rabbits': rabbits,
    }
    return render(request, 'bunnyapp/game.html', context)


def initialize_forest(forest):
    # List to track already used positions
    used_positions = set()

    # Create one hunter
    hunter = Hunter.objects.create(
        forest=forest,
        bullet=BULLET_NUMBER,
        hunger=0,
        kilometers=0,
        position_x=HUNTER_POSITION_X,
        position_y=HUNTER_POSITION_Y,
        message=""
    )
    used_positions.add((HUNTER_POSITION_X, HUNTER_POSITION_Y))

    # Create trees
    for _ in range(TREES_NUMBER):
        while True:
            position_x = random.randint(0, forest.size - 1)
            position_y = random.randint(0, forest.size - 1)
            if (position_x, position_y) not in used_positions:
                Tree.objects.create(
                    forest=forest,
                    position_x=position_x,
                    position_y=position_y
                )
                used_positions.add((position_x, position_y))
                break

    # Create burrows
    for _ in range(BURROWS_NUMBER):
        while True:
            position_x = random.randint(0, forest.size - 1)
            position_y = random.randint(0, forest.size - 1)
            if (position_x, position_y) not in used_positions:
                Burrow.objects.create(
                    forest=forest,
                    position_x=position_x,
                    position_y=position_y
                )
                used_positions.add((position_x, position_y))
                break

    # Create rabbits
    for _ in range(RABBITS_NUMBER):
        while True:
            position_x = random.randint(0, forest.size - 1)
            position_y = random.randint(0, forest.size - 1)
            if (position_x, position_y) not in used_positions:
                Rabbit.objects.create(
                    forest=forest,
                    speed=1,
                    color="brown",
                    kilometers=0,
                    position_x=position_x,
                    position_y=position_y,
                    message=""
                )
                used_positions.add((position_x, position_y))
                break
