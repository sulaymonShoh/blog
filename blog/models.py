from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CASCADE


class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, AbstractModel):
    avatar = models.ImageField(upload_to='avatars')


class Post(AbstractModel):
    title = models.CharField(max_length=128)
    content = models.TextField()
    published_at = models.DateField()
    is_active = models.BooleanField(default=False)
    author = models.ForeignKey("blog.User", CASCADE, 'posts')
