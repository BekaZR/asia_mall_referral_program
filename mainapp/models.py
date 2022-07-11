from django.db import models
from django.contrib.auth.models import AbstractUser
from mainapp.managers import CustomUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from mainapp.servises import create_token
from datetime import datetime, timedelta


class User(AbstractUser):
    phone_number = models.CharField('phone number', unique=True, max_length=15)
    username = None
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        
    def __str__(self):
        return f"{self.phone_number}"


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, 
        related_name='users_profile', verbose_name='пользователь'
    )
    username = models.CharField(
        max_length=31,
        verbose_name="ник", null=True
        )
    about = models.CharField(
        max_length=100, null=True, 
        blank=True, verbose_name='о себе'
        )
    recomennded_by = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, 
        null=True, blank=True, related_name='users_recomenndeds'
        )
    updated = models.DateTimeField(
        auto_now=True, verbose_name='дата изменения'
        )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='дата создания'
        )
    
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
    
    def __str__(self):
        return f"{self.user.phone_number}"


class ReferralProgram(models.Model):
    user = models.OneToOneField(
        Profile, on_delete=models.CASCADE,
        related_name="user_refferals"
    )
    token = models.CharField(max_length=200, blank=True, null=True)
    created_add = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Реферал"
        verbose_name = "Рефералы"
        
    def __str__(self):
        return f"{self.token}"


@receiver(post_save, sender=User)
def create_connected_models(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Profile)
def create_connected_models(sender, instance, created, **kwargs):
    if created:
        ReferralProgram.objects.create(user=instance, token=create_token(token=instance.pk))