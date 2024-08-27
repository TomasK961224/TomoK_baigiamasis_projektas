from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from tinymce.models import HTMLField
from PIL import Image

# Create your models here.
class AnimalCategory(models.Model):
    name = models.CharField('Name of animal category',max_length=200)
    description = HTMLField(null=True)

    def __str__(self):
        return self.name

class Animal(models.Model):
    category = models.ManyToManyField(AnimalCategory, help_text='Aprašykime gyvūnus priklausančius kategorijai')
    name = models.CharField('Name of animal', max_length=200)
    scientific_name = models.CharField('Scientific name', max_length=200)
    description = HTMLField(null=True)
    habitat = models.TextField('Habitat of animal', max_length=2000)
    diet = models.TextField('Diet of animal', max_length=2000)
    conservation_status = models.TextField('Status of conservation', max_length=1000)
    image = models.ImageField('Image', upload_to='covers', null=True)

    def display_category(self):
        return ', '.join(category.name for category in self.category.all()[:3])

    display_category.short_description = 'Animal Category'

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
    animal = models.ForeignKey('Animal', on_delete=models.CASCADE, related_name='blog_posts', null=True, blank=True)

    def __str__(self):
        return self.title

class AnimalReview(models.Model):
    animal = models.ForeignKey('Animal', on_delete=models.SET_NULL, null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Comment', max_length=2000)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = 'Comments'
        ordering = ['-date_created']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default="default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)