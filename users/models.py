from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import send_welcome_email  # Celery task
# Create your models here.


class User(AbstractUser):
    ROLE_CHOICE = (
        ('client', 'Client'),
        ('freelancer', 'Freelancer')
    )
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['role','password', 'username']

    def __str__(self):
        return f"{self.username} ({self.role})"
    
    
    
class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)


    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


@receiver(post_save, sender=User)
def send_welcome_email_signal(sender, instance, created, **kwargs):
    if created:
        send_welcome_email(instance.email, instance.username)
