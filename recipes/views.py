from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Recipe, RecipesUser
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
import requests
from bs4 import BeautifulSoup




# Create your views here.

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, "recipes/recipe_list.html", {"recipes": recipes})

def recipe_detail(request, pk):
    recipes = get_object_or_404(Recipe, pk=pk)
    return render(request, "recipes/recipe_details.html", {"recipes": recipes})

def register(request):
    if request.method == "GET":
        return render(request, "recipes/register.html")

    firstname = request.POST['fname']
    lastname = request.POST['lname']
    username = request.POST['username']
    gender = request.POST['gender']
    email = request.POST['email']
    password = request.POST['password']
    country = request.POST['country']
    user = User.objects.create_user(
                first_name = firstname, 
                last_name = lastname, 
                username = username,
                password = password,
                email = email)
    user.save()
    recipesuser = RecipesUser(user = user, country = country, gender = gender)
    recipesuser.save()
    return HttpResponseRedirect('/login/')





def recipe_add(request):

    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, "recipes/recipe_add.html")
        
        else:
            title = request.POST.get('title')
            user = request.user
            ru = get_object_or_404(RecipesUser, user=user)
            ingredients = request.POST.get('ingredients')
            instructions = request.POST.get('instructions')
            prep_time = request.POST.get('prep_time')

            recipe = Recipe(
                        title = title,
                        ingredients = ingredients,
                        instructions = instructions,
                        prep_time = prep_time,
                        creator=ru
                        )
            recipe.save()
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect("/login/")

def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        ingredients = request.POST.get('ingredients')
        instructions = request.POST.get('instructions')
        prep_time = request.POST.get('prep_time')

        if title and ingredients and instructions and prep_time:
            try:
                recipe.title = title
                recipe.ingredients = ingredients
                recipe.instructions = instructions
                recipe.prep_time = int(prep_time)
                recipe.save()
                return HttpResponseRedirect(f'/recipe/{recipe.id}/')
            except ValueError:
                return HttpResponse("Invalid data")
        else:
            return HttpResponse("Missing required fields")
    return render(request, 'recipes/recipe_edit.html', {'recipe': recipe,})

def profile(request):
    if request.user.is_authenticated:
        profile = get_object_or_404(RecipesUser, user=request.user)
        recipes = Recipe.objects.filter(creator__user=request.user)
        return render(request, "recipes/profile.html", {"profile": profile, "recipes": recipes})
    else:
        return HttpResponseRedirect("/login")

def rate(request, pk):
    if request.user.is_authenticated:
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            rating = request.POST.get('rating')
            if rating:
                try:
                    rating = float(rating)
                    if 0 <= rating <= 5:
                        new_count = recipe.count + 1
                        new_rate = (recipe.rate * recipe.count + rating) / new_count
                        recipe.rate = new_rate
                        recipe.count = new_count
                        recipe.save()
                        return HttpResponseRedirect(f'/recipe/{pk}/')  
                except ValueError:
                    return HttpResponse("write number 1-5")
        return render(request, 'recipes/rate.html', {'recipe': recipe})
    else:
        return HttpResponseRedirect("/login/")


def log_in(request):
    if request.method == "GET":
        return render(request, "recipes/login.html", {})
    
    usr = request.POST['username']
    pswd = request.POST['password']
 
    user = authenticate(username=usr, password=pswd)
    if user:
        login(request, user)
        return HttpResponseRedirect("/")
    
    return render(request, "recipes/login.html", {"error": "username or password is wrong"})

def log_out(request):
    logout(request)
    return HttpResponseRedirect("login")

