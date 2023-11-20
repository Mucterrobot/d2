from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator


# Create your models here.


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.post_set = None

    def update_rating(self):
        post_rating = sum([p.rating * 3 for p in self.post_set.all()])
        comment_rating = sum([c.rating for c in self.user.commpent_set.all()])
        comment_post_rating = sum([c.rating for p in self.post_set.all() for c in p.comment_set.all()])
        self.rating = post_rating + comment_rating + comment_post_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    TYPE_CHOICES = (
        ('N', 'News'),
        ('A', 'Article'),
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return Truncator(self.text).chars(124, truncate='...')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
