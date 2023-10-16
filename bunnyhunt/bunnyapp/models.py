from django.db import models

from bunnyapp.constants import HUNTER_POSITION_X, HUNTER_POSITION_Y, DANGER_DISTANCE
from bunnyapp.controller.bunnyapp.trigonometry import distance


class Forest(models.Model):
    size = models.IntegerField()
    objects = models.Manager()


class Hunter(models.Model):
    forest = models.ForeignKey(Forest, on_delete=models.DO_NOTHING)
    bullet = models.IntegerField()
    hunger = models.IntegerField()
    kilometers = models.IntegerField()
    position_x = models.IntegerField()
    position_y = models.IntegerField()
    message = models.CharField(max_length=24, default="None")
    objects = models.Manager()

    def hunt(self):
        """
        To check if the hunter is one square away from a rabbit
        :return: True if the hunter is next to a rabbit, False otherwise.
        """
        rabbits = Rabbit.objects.all()
        for rabbit in rabbits:
            rabbit_distance = distance(self.position_x, self.position_y, rabbit.position_x, rabbit.position_y)
            if rabbit_distance < 2:
                return True
        return False


class Rabbit(models.Model):
    forest = models.ForeignKey(Forest, on_delete=models.DO_NOTHING)
    speed = models.IntegerField()
    color = models.CharField(max_length=10)
    kilometers = models.IntegerField()
    position_x = models.IntegerField()
    position_y = models.IntegerField()
    message = models.CharField(max_length=24, default="None")
    objects = models.Manager()

    def pursued(self):
        hunter = Hunter.objects.first()
        hunter_distance = distance(self.position_x, self.position_y, hunter.position_x, hunter.position_y)
        if hunter_distance < DANGER_DISTANCE:
            return True
        return False


class Tree(models.Model):
    forest = models.ForeignKey(Forest, on_delete=models.DO_NOTHING)
    position_x = models.IntegerField()
    position_y = models.IntegerField()
    objects = models.Manager()


class Burrow(models.Model):
    forest = models.ForeignKey(Forest, on_delete=models.DO_NOTHING)
    position_x = models.IntegerField()
    position_y = models.IntegerField()
    objects = models.Manager()

