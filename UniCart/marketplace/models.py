from django.db import models
from django.contrib.auth.models import User

class University(models.Model):
    name     = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    logo     = models.ImageField(
                   upload_to='university_logos/',
                   null=True, blank=True
               )
    def __str__(self):
        return self.name

class Profile(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE)
    university = models.ForeignKey(
                     University, on_delete=models.SET_NULL,
                     null=True, blank=True
                 )
    photo      = models.ImageField(
                     upload_to='profile_photos/',
                     null=True, blank=True
                 )
    is_seller  = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Listing(models.Model):
    seller      = models.ForeignKey(
                      User, on_delete=models.CASCADE,
                      related_name='listings'
                  )
    title       = models.CharField(max_length=120)
    description = models.TextField()
    image       = models.ImageField(
                      upload_to='listing_images/',
                      null=True, blank=True
                  )
    date = models.DateTimeField(auto_now_add=True)
    categories  = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return f"{self.title} by {self.seller.username}"


