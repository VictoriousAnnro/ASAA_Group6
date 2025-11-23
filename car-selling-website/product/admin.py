from django.contrib import admin
from product.models import Car, CarVariants

# Register your models here.
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description']

@admin.register(CarVariants)
class CarVariantsAdmin(admin.ModelAdmin):
    list_display = ['car', 'car_model', 'car_engine', 'car_color', 'car_price']
