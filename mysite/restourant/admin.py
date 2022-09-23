from django.contrib import admin
from.models import Balance, Dish,Order,Table
# Register your models here.

admin.site.register(Dish)
admin.site.register(Table)
admin.site.register(Order)
admin.site.register(Balance)


