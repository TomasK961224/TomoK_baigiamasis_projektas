from django.shortcuts import render
from django.http import HttpResponse
from .models import AnimalCategory, Animal, Tag, BlogPost
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.shortcuts import render, reverse, get_object_or_404, reverse
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin

from .forms import AnimalReviewForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
# Create your views here.

def index(request):
    num_animal_categories = AnimalCategory.objects.all().count()
    num_animals = Animal.objects.all().count()
    num_tags = Tag.objects.all().count()
    num_blogposts = BlogPost.objects.all().count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_animal_categories': num_animal_categories,
        'num_animals': num_animals,
        'num_tags': num_tags,
        'num_blogposts': num_blogposts,
        'num_visits': num_visits,
    }
    return render(request, 'index.html', context=context)


def animal_categories(request):
    paginator = Paginator(AnimalCategory.objects.all(), 3)
    page_number = request.GET.get('page')
    animal_categories = paginator.get_page(page_number)
    context = {
        'animal_categories': animal_categories
    }
    return render(request, 'animal_categories.html', context=context)

def animals_in_category(request, id):
    single_category = get_object_or_404(AnimalCategory, pk=id)
    return render(request, 'animals_in_category.html', {'animals_in_category': single_category})

class AnimalListView(generic.ListView):
    model = Animal
    paginate_by = 1
    template_name = 'animal_list.html'

class AnimalDetailView(FormMixin, generic.DetailView):
    model = Animal
    template_name = 'animal_detail.html'
    form_class = AnimalReviewForm

    # nurodome, kur atsidursime komentaro sėkmės atveju.
    def get_success_url(self):
        return reverse('book-detail', kwargs={'pk': self.object.id})

    # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # štai čia nurodome, kad knyga bus būtent ta, po kuria komentuojame, o vartotojas bus tas, kuris yra prisijungęs.
    def form_valid(self, form):
        form.instance.book = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(AnimalDetailView, self).form_valid(form)

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


class UserPostsListView(LoginRequiredMixin, generic.ListView):
    model = BlogPost
    template_name = 'user_posts.html'
    paginate_by = 10

    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user).order_by('created_at')

@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')

@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profile updated")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context)

class UserPostDetailView(LoginRequiredMixin, DetailView):
    model = BlogPost
    template_name = 'user_post.html'

    def get_absolute_url(self):
        """Nurodo konkretaus aprašymo galinį adresą"""
        return reverse('animal_detail', args=[str(self.id)])

class UserPostCreateView(LoginRequiredMixin, generic.CreateView):
    model = BlogPost
    fields = ['title', 'content']
    success_url = "/animals/blog_posts_list/"
    template_name = 'user_post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class UserPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = BlogPost
    fields = ['title', 'content']
    success_url = "/animals/blog_posts_list/"
    template_name = 'user_post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        blogpost = self.get_object()
        return self.request.user == blogpost.author

class UserPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = BlogPost
    success_url = "/animals/blog_posts_list/"
    template_name = 'user_post_delete.html'

    def test_func(self):
        blogpost = self.get_object()
        return self.request.user == blogpost.author

