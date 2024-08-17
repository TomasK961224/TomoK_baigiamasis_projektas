from django.contrib import admin
from .models import AnimalCategory, Animal, Tag, BlogPost

# Register your models here.
class AnimalCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')

class AnimalAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'scientific_name', 'description', 'habitat', 'diet', 'conservation_status', 'image')
    list_filter = ('category', 'name', 'scientific_name')
    search_fields = ('id', 'name', 'scientific_name')

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_at', 'author', 'excerpt', 'featured_image', 'status', 'views_count', 'animal')

admin.site.register(AnimalCategory, AnimalCategoryAdmin)
admin.site.register(Animal, AnimalAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(BlogPost, BlogPostAdmin)