from django.db import models
from django.contrib.auth.models import AbstractUser



class ProfileUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('field_owner', 'Field Owner'),
        ('regular_user', 'Regular User'),
    )
    username = models.CharField(max_length=255,unique=True)
    email = models.EmailField(max_length=255)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='regular_user')
    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username


class FootballField(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(ProfileUser,on_delete=models.CASCADE)
    address = models.TextField()
    contact = models.IntegerField()
    image = models.ImageField(upload_to='field_images/', blank=True, null=True)
    hourly_price = models.DecimalField(max_digits=6, decimal_places=2)
    bron = models.BooleanField(default=False)
    date = models.DateField()
    
    
    def __str__(self):
        return self.name


    
