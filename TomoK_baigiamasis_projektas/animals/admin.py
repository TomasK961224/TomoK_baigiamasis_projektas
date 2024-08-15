from django.contrib import admin
from .models import AnimalCategory, Animal, Tag, BlogPost

# Register your models here.

admin.site.register(AnimalCategory)
admin.site.register(Animal)
admin.site.register(Tag)
admin.site.register(BlogPost)