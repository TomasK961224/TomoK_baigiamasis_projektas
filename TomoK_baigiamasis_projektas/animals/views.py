from django.shortcuts import render
from django.http import HttpResponse
from .models import AnimalCategory, Animal, Tag, BlogPost
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
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
    paginator = Paginator(AnimalCategory.objects.all(), 2)
    page_number = request.GET.get('page')
    animal_categories = paginator.get_page(page_number)
    context = {
        'animal_categories': animal_categories
    }
    return render(request, 'animal_categories.html', context=context)

def animals_in_category(request, id):
    single_category = get_object_or_404(Animal, pk=id)
    return render(request, 'animals_in_category.html', {'animals_in_category': single_category})

class AnimalListView(generic.ListView):
    model = Animal
    paginate_by = 1
    template_name = 'animal_list.html'

class AnimalDetailView(generic.DetailView):
    model = Animal
    template_name = 'animal_detail.html'

def search(request):
    """
    paprasta paieška. query ima informaciją iš paieškos laukelio,
    search_results prafiltruoja pagal įvestą tekstą knygų pavadinimus ir aprašymus.
    Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raidės
    didžiosios/mažosios.
    """
    query = request.GET.get('query')
    search_results = Animal.objects.filter(Q(name__icontains=query) | Q(scientific_name__icontains=query))
    return render(request, 'search.html', {'animals': search_results, 'query': query})