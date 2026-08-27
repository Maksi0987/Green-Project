from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Користувач',
        related_name='profile'
    )
    bio = models.TextField(max_length=500, blank=True, verbose_name='Коротко про себе')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Фото профілю')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата народження')
    location = models.CharField(max_length=60, blank=True, verbose_name='Місцезнаходження')
    website = models.URLField(blank=True, verbose_name='Особистий сайт')

    class Meta:
        verbose_name = 'Профіль'
        verbose_name_plural = 'Профілі'

    def __str__(self):
        return f"Особистий кабінет: {self.user.username}"


@receiver(post_save, sender=User)
def trigger_profile_creation(sender, instance, created, **kwargs):
    """Автоматично генерує профіль при створенні нового користувача"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def trigger_profile_save(sender, instance, **kwargs):
    """Безпечно зберігає профіль, створюючи його, якщо він раптом зник"""
    Profile.objects.get_or_create(user=instance)
    instance.profile.save()