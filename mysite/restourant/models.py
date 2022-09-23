from tabnanny import verbose
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Dish(models.Model):
    dish_name=models.TextField(blank=True,unique=True,verbose_name="name of the dish")
    dish_category=models.TextField(blank=True,verbose_name="type of dish")
    dish_price=models.FloatField(blank=True,validators=[MinValueValidator(0)],verbose_name="price of the dish")
    available=models.BooleanField(default=True)

class Menu(models.Model):
    dish=models.ForeignKey(Dish,on_delete=models.CASCADE)
    

class Table(models.Model):
    table_id=models.PositiveIntegerField(primary_key=True,validators=[MaxValueValidator(9999999999)],verbose_name="id of the table")
    table_people=models.PositiveIntegerField(default=0,verbose_name="number of people in the table")

class Order(models.Model):
    dish=models.ForeignKey(Dish,on_delete=models.CASCADE)
    table=models.ForeignKey(Table,on_delete=models.CASCADE)
    done=models.BooleanField(default=False,verbose_name="dish done by the kitchen")

class Balance(models.Model):
    data=models.DateField(blank=True,verbose_name='datetime of payment')
    price=models.FloatField(blank=True,verbose_name='price of one dinner/lunch')