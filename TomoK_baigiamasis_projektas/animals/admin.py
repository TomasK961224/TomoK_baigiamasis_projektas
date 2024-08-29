from django.contrib import admin
from .models import AnimalCategory, Animal, Tag, BlogPost, AnimalReview, Profile

# Register your models here.
class AnimalCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')

class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'scientific_name', 'display_category', 'description', 'habitat', 'diet', 'conservation_status', 'image')
    list_filter = ('name', 'scientific_name')
    search_fields = ('id', 'name', 'scientific_name')

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_at', 'author', 'featured_image', 'status', 'animal')

class AnimalReviewAdmin(admin.ModelAdmin):
    list_display = ('animal', 'date_created', 'reviewer', 'content')

admin.site.register(AnimalCategory, AnimalCategoryAdmin)
admin.site.register(Animal, AnimalAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(AnimalReview, AnimalReviewAdmin)
admin.site.register(Profile)