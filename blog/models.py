from django.db import models
from django.contrib import admin
from django.utils.text import slugify
from user_profile.models import User
from django.utils.html import format_html

from utils import *

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=150)
    created_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True)

    @admin.display(description="Number")
    def blogs_number(self):
        return self.category_blogs.count()

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Tag(models.Model):
    title = models.CharField(max_length=150)
    created_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True)

    @admin.display(description="Number")
    def blogs_number(self):
        return self.tag_blogs.count()

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Blog(models.Model):
    title = models.CharField(
        max_length=250
    )

    content = models.TextField()

    banner = models.ImageField(
        upload_to="blog_banner"
    )

    author = models.ForeignKey(
        User,
        related_name='author_blogs',
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        related_name='category_blogs',
        on_delete=models.CASCADE
    )

    tags = models.ManyToManyField(
        Tag,
        related_name='tag_blogs',
        blank=True
    )

    like = models.ManyToManyField(
        User,
        # related_name="like_user",
        blank=True,
        through='Like'
    )

    created_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, unique=True)

    @admin.display(description="Preview")
    def show_banner(self):
        return format_html('<img src="/%s" width="150" height="150" />' % (self.banner))
    
    def formatted_date(self):
        return datetime_format(self.created_date)
    
    def process_image(self):
        if not check_image_size(self.banner.path, 1200, 630):
            new_path = get_random_image_name(self.banner.path)
            resize_img(self.banner.path, new_path, 1200, 630)
            self.banner.name = f"blog_banner/{new_path.split('\\')[-1]}"
    
    def generate_slug(self, title):
        self.slug = slugify(title)
        print(self.slug)

        if Blog.objects.filter(slug=self.slug).exists():
            self.generate_slug(f"{self.title} {get_random_slug_suffix()}")

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.generate_slug(self.title)
            
        super().save(*args, **kwargs)
        self.process_image()
        super().save(*args, **kwargs)
    

class Comment(models.Model):
    text = models.TextField()

    user = models.ForeignKey(
        User,
        related_name="comment_user",
        on_delete=models.CASCADE
    )

    blog = models.ForeignKey(
        Blog,
        related_name="blog_comments",
        on_delete=models.CASCADE
    )

    created_date = models.DateTimeField(auto_now_add=True)

    def formatted_date(self):
        return datetime_format(self.created_date)


    # confirmed = models.BooleanField(default=True)

    def __str__(self):
        return self.text
    

class Reply(models.Model):
    text = models.TextField()

    user = models.ForeignKey(
        User,
        related_name="reply_user",
        on_delete=models.CASCADE
    )

    comment = models.ForeignKey(
        Comment,
        related_name="comment_reply",
        on_delete=models.CASCADE
    )

    created_date = models.DateTimeField(auto_now_add=True)

    def formatted_date(self):
        return datetime_format(self.created_date)


    # confirmed = models.BooleanField(default=True)

    def __str__(self):
        return self.text


class Like(models.Model):
    user = models.ForeignKey(
        User,
        # related_name="user_like",
        on_delete=models.CASCADE
    )

    blog = models.ForeignKey(
        Blog,
        related_name="blog_like",
        on_delete=models.CASCADE
    )

    created_date = models.DateTimeField(auto_now_add=True)
