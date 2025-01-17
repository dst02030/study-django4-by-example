from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = Post.Status.PUBLISHED)

class Post(models.Model):
    
    objects = models.Manager()
    published = PublishedManager()
    
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    
    title = models.CharField(max_length = 250)
    slug = models.SlugField(max_length = 250)
    author = models.ForeignKey(User,
                               on_delete = models.CASCADE,
                               related_name = 'blog_post')
    body = models.TextField()
    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length = 2,
                              choices = Status.choices,
                              default = Status.DRAFT)
    
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields = ['-publish']),
        ]
        # default_manager_name = objects
    
    def __str__(self):
        return self.title