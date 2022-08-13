from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    def __str__(self):
        return self.user.username # displays username instead of Profile obj

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dp = models.ImageField(default='404.png', upload_to='profile')
    contact = models.CharField(max_length=15, default="6385674986")

