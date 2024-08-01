from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from .managers import CustomUserManager

from utils import *

# Create your models here.
class User(AbstractUser):
    username = models.CharField(
        "username",
        max_length=150,
        unique=True,
        blank=True,
        null=True
    )
    
    email = models.EmailField(
        "email address",
        unique=True
    )

    profile_image = models.ImageField(
        null=True,
        blank=True,
        upload_to="profile_image",
        default="./profile_image/man.png"
    )

    followers = models.ManyToManyField("Follow")

    slug = models.SlugField(blank=True, unique=True)

    # USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def process_image(self):
        if not check_image_size(self.profile_image.path,400, 400):
            new_path = get_random_image_name(self.profile_image.path)
            resize_img(self.profile_image.path, new_path, 400, 400)
            self.profile_image.name = f"profile_image/{new_path.split('/')[-1]}"

    def generate_slug(self, username):
        self.slug = slugify(username)

        if User.objects.filter(slug=self.slug).exists():
            self.generate_slug(f"{self.username} {get_random_slug_suffix()}")
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.generate_slug(self.username)
        super().save(*args, **kwargs)
        if self.profile_image:
            self.process_image()
        super().save(*args, **kwargs)

class Follow(models.Model):
    followed = models.ForeignKey(
        User,
        related_name="user_followers",
        on_delete=models.CASCADE
    )

    follower = models.ForeignKey(
        User,
        related_name="user_followed",
        on_delete=models.CASCADE
    )

    created_date = models.DateTimeField(auto_now_add=True)        
    
