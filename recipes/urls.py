from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('register/', views.register, name='register'),
    path('recipe_add/', views.recipe_add, name='recipe_add'),
    path('profile/', views.profile, name='profile'),
    path("login/", views.log_in, name="login"),
    path("logout", views.log_out, name="logout"),
    path('rate/<int:pk>/', views.rate, name='rate'),
    path('recipe_edit/<int:recipe_id>/', views.recipe_edit, name='recipe_edit'),
    path("scraping_add/", views.scraping_add, name="scraping_add"),
    path("comment/<int:pk>/", views.comment, name="comment"),
]