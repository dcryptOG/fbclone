from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):
    # create relationship (inherit from User)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Add any additional attributes you want
    portfolio_site = models.URLField(blank=True)
    # pip install pillow to use this
    # optional" pip install pillow --global-option:

    profile_pic = models.ImageField(upload_to='patrons_app/profile_pics', blank=True)

    def __str__(self):
        # built-in attribute of django.contrib.auth.models.User
        return self.user.username
