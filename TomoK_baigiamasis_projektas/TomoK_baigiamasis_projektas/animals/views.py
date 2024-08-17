from django.shortcuts import render
from django.http import HttpResponse
from .models import AnimalCategory, Animal, Tag, BlogPost
# Create your views here.

def index(request):
    num_animal_categories = AnimalCategory.objects.all().count()
    num_animals = Animal.objects.all().count()
    num_tags = Tag.objects.all().count()
    num_blogposts = BlogPost.objects.all().count()

    context = {
        'num_animal_categories': num_animal_categories,
        'num_animals': num_animals,
        'num_tags': num_tags,
        'num_blogposts': num_blogposts,
    }

    return render(request, 'index.html', context=context)


def animal_categories(request):
    animal_categories = AnimalCategory.objects.all()
    context = {
        'animal_categories': animal_categories
    }
    print(animal_categories)
    return render(request, 'animal_categories.html', context=context)