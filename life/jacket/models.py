from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have a username')
        
        user = self.model(
            username=username.lower(),
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)  # Django handles password hashing
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'
    
    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin

class Location(models.Model):
    location_name = models.CharField(max_length=100)
    location_id = models.CharField(max_length=20)
    district = models.CharField(max_length=50)
    nearest_railway_station = models.CharField(max_length=100)
    distance_from_railway_station = models.FloatField()
    nearest_airport = models.CharField(max_length=100)
    distance_from_airport = models.FloatField()
    
    def __str__(self):
        return self.location_name

class TravelPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.CharField(max_length=255)  # Path to image or URL
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    posted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Review(models.Model):
    rating = models.IntegerField()
    comment = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    posted = models.DateTimeField(auto_now_add=True)
    travel_post = models.ForeignKey(TravelPost, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Review by {self.user_id.username} on {self.travel_post.title}"