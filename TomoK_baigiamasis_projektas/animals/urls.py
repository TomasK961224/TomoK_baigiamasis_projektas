from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.animal_categories, name='animal_categories'),
    path('categories/<int:id>', views.animals_in_category, name='animals_in_category'),
    path('animals_list/', views.AnimalListView.as_view(), name='animals_list'),
    path('animals_list/<int:pk>', views.AnimalDetailView.as_view(), name='animal_detail'),
    path('search/', views.search, name='search'),
]