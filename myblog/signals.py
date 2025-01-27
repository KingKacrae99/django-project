from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserSettings, Post, Notification


User = get_user_model()
@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        UserSettings.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_settings(sender, instance, **kwargs):
    instance.settings.save()

# Notification Signal
@receiver(post_save, sender=Post)
def notify_new_post(sender, instance, created, **kwargs):
    if created:
       if instance.status == 'draft':
            Admins = User.objects.filter(is_admin=True)
            writer = instance.author
            for admin in Admins:
                Notification.objects.create(
                    recipient=admin,
                    sender= writer,
                    notification_type = 'draft',
                    post=instance,
                    message=(
                        f"Unpublished post titled '{instance.title}' "
                        f"created by {writer.username}."
                    )
                )
    elif  created and instance.status == 'published':
            user = User.objects.get(id=instance.author.id)
            liked_users = User.objects.filter(posts__author=user).distinct()
            for liked_user in liked_users:
                if not liked_user.is_admin and instance.is_trending == False:
                        Notification.objects.create(
                            recipient= liked_user,
                            sender =instance.author,
                            notification_type= 'new_post',
                            post=instance,
                            message=(
                                f"A new post titled '{instance.title}' has been published by {instance.author.username}.{instance.dop}"
                            )
                        )