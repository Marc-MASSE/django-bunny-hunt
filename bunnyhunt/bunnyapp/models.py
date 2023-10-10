from django.db import models


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
    objects = models.Manager()

    def hunt(self):
        # Something
        pass


class Rabbit(models.Model):
    forest = models.ForeignKey(Forest, on_delete=models.DO_NOTHING)
    speed = models.IntegerField()
    color = models.CharField(max_length=10)
    kilometers = models.IntegerField()
    position_x = models.IntegerField()
    position_y = models.IntegerField()
    objects = models.Manager()

    def flee(self):
        # Something
        pass


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

