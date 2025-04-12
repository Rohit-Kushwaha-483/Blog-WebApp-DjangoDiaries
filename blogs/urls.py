from django.urls import path
from . import views

urlpatterns = [
    path('<int:category_id>/', views.posts_by_category, name='posts_by_category'),
    path('author/<str:username>/', views.posts_by_author, name='posts_by_author'),
]
