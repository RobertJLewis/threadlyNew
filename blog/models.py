from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse

User = get_user_model()

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title  = models.CharField(max_length=200, unique=True)
    slug   = models.SlugField(max_length=210, unique=True, editable=False)
    hero_image = models.ImageField(upload_to="posts/hero/", blank=True)
    body   = models.TextField()           # store Markdown or HTML
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    published   = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:210]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.slug])

    def __str__(self):
        return self.title

class Slide(models.Model):
    title     = models.CharField(max_length=200)
    image     = models.ImageField(upload_to="slides/")
    timestamp = models.DateTimeField(auto_now_add=True)
    summary   = models.CharField(max_length=300, blank=True)  

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return self.title
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, editable=False)
    icon = models.CharField(max_length=50, blank=True)     # e.g. "bi-chat-dots"
    image = models.ImageField(upload_to="categories/")     # your static could also work

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Thread(models.Model):
    category   = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="threads")
    author     = models.ForeignKey(User, on_delete=models.CASCADE)
    title      = models.CharField(max_length=200)
    body       = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


class Comment(models.Model):
    thread     = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="comments")
    author     = models.ForeignKey(User, on_delete=models.CASCADE)
    body       = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class ThreadReaction(models.Model):
    LIKE  = 1
    DISLIKE = -1
    REACTION_CHOICES = [(LIKE, "Like"), (DISLIKE, "Dislike")]

    thread    = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="reactions")
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    value     = models.SmallIntegerField(choices=REACTION_CHOICES)

    class Meta:
        unique_together = ("thread", "user")

