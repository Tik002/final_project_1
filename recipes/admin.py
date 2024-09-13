from django.contrib import admin
from .models import Recipe, RecipesUser 

# Register your models here.

admin.site.register(Recipe)
admin.site.register(RecipesUser)