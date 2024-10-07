from django.contrib import admin
from .models import Recipe, RecipesUser, Comment

# Register your models here.

admin.site.register(Recipe)
admin.site.register(RecipesUser)
admin.site.register(Comment)
