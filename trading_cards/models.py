import random

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import Profile, ProfileType


class Card(models.Model):
    yugioh_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    img = models.URLField()
    img_small = models.URLField()
    profiles = models.ManyToManyField(Profile, related_name='deck')


@receiver(post_save, sender=User)
def create_profile(sender, created, instance, **kwargs):
    if created:
        origin = random.choice(ProfileType.objects.all())
        profile = Profile.objects.create(user=instance, origin=origin)
        profile.deck.add(*random.sample(list(Card.objects.all()), k=26))
