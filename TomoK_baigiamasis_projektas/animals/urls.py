from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.animal_categories, name='animal_categories'),
    path('categories/<int:id>', views.animals_in_category, name='animals_in_category'),
    path('animals_list/', views.AnimalListView.as_view(), name='animals_list'),
    path('animals_list/<int:pk>', views.AnimalDetailView.as_view(), name='animal_detail'),
    path('blog_posts_list/', views.UserPostsListView.as_view(), name='user_posts'),
    path('blog_posts_list/<int:pk>', views.UserPostDetailView.as_view(), name='user_post'),
    path('blog_posts_list/new', views.UserPostCreateView.as_view(), name='user_post_new'),
    path('blog_posts_list/<int:pk>/update', views.UserPostUpdateView.as_view(), name='user_post_update'),
    path('blog_posts_list/<int:pk>/delete', views.UserPostDeleteView.as_view(), name='user_post_delete'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]