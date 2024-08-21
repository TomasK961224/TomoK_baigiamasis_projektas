from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class AnimalCategory(models.Model):
    name = models.CharField('Name of animal category',max_length=200)
    description = models.TextField('Description of animal category',max_length=1000)

    def __str__(self):
        return self.name

class Animal(models.Model):
    category = models.ForeignKey(AnimalCategory, on_delete=models.SET_NULL, null=True)
    name = models.CharField('Name of animal', max_length=200)
    scientific_name = models.CharField('Scientific name', max_length=200)
    description = models.TextField('Description of animal', max_length=2000)
    habitat = models.TextField('Habitat of animal', max_length=2000)
    diet = models.TextField('Diet of animal', max_length=2000)
    conservation_status = models.CharField('Status of conservation', max_length=200)
    image = models.ImageField('Image', upload_to='covers', null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField('Title of Post', max_length=200)
    content = HTMLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ManyToManyField('Tag', blank=True)
    excerpt = models.TextField(blank=True)
    featured_image = models.ImageField('Featured image', upload_to='covers', blank=True, null=True)
    STATUS_CHOICES = (
        ('a', 'Draft'),
        ('b', 'Published'),
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        blank=True,
        default='a',
        help_text='Status',
    )
    views_count = models.PositiveIntegerField(default=0)
    animal = models.ForeignKey('Animal', on_delete=models.CASCADE, related_name='blog_posts', null=True, blank=True)

    def __str__(self):
        return self.title