from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile


@receiver(post_save, sender=User)
def user_create(sender, instance, created, **kwargs):
    if created:
        my_profile = Profile.objects.create(
            user=instance,
            username=instance.username,
            email=instance.email,
            name=instance.first_name,
        )

        send_mail(
            "Welcome to Example",
            "You account was successfully created, great work",
            settings.EMAIL_HOST_USER,
            [my_profile.email],
            False
        )


@receiver(post_delete, sender=Profile)
def profile_deleted(sender, instance, **kwargs):
    print("profile deleted")
    instance.user.delete()
    print("deleting user")


@receiver(post_save, sender=Profile)
def edit_profile(sender, instance, created, **kwargs):
    if created is False:
        print("profile edited")
        profile = instance
        user = profile.user
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()
