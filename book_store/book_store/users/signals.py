from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

from django.contrib import messages
from django.contrib.auth.signals import user_logged_in, user_logged_out


def logged_in_message(sender, user, request, **kwargs):
    messages.info(
        request, f"Witaj {request.user}, jesteś zalogowany/a. Teraz możesz dodawać komentarze, oceniań oraz wypożyczać książki :) ")


def logout_message(sender, user, request, **kwargs):
    messages.info(
        request, f"Pomyślnie się wylogowałeś, do zobaczenia {request.user}")


user_logged_out.connect(logout_message)
user_logged_in.connect(logged_in_message)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    instance.profile.save()
