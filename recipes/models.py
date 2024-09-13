from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class RecipesUser(models.Model):
    OPTION_ONE = 'men'
    OPTION_TWO = 'women'
    OPTION_THREE = 'other'
    MY_CHOICES = [
        (OPTION_ONE, 'men'),
        (OPTION_TWO, 'women'),
        (OPTION_THREE, 'other')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=20)
    gender = models.CharField(max_length=20, choices=MY_CHOICES, default=OPTION_THREE,)

    def __str__(self):
        return self.user.username

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    ingredients = models.TextField()
    instructions = models.TextField()
    rate = models.FloatField(default=0)
    count = models.IntegerField(default=0)
    prep_time = models.IntegerField()
    creator = models.ForeignKey(RecipesUser, on_delete=models.CASCADE, null=True)


    def __str__(self) -> str:
        return self.title



