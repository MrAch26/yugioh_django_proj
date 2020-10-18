from django.db import models


class Cards(models.Model):
    id = models.IntegerField()
    name = models.CharField(max_length=50)
    img = models.URLField()


class Deck(models.Model):
    cards = models.ManyToManyField(Cards)


