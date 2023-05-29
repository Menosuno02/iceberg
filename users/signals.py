from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from friend.models import FriendList

from .models import Profile, Relationship

""" Crea perfil cuando usuario crea cuenta """
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

""" Guarda perfil cuando usuario actualiza su perfil """
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

""" Guardado de relación de amistad """
@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, created, instance, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        sender_.friends.add(receiver_.user)
        receiver_.friends.add(sender_.user)
        sender_.save()
        receiver_.save()

""" Crear lista de amigos cuando usuario crea cuenta """
@receiver(post_save, sender=User)
def create_friendlist(sender, instance, created, **kwargs):
    if created:
        FriendList.objects.create(user=instance)