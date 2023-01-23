from django.contrib import admin
from .models.product import Product
from .models.category import Categories
from .models.customer import Customer
from .models.orders import Order
# Register your models here.

class AdminProduct(admin.ModelAdmin):
    list_display = ['name','price', 'category']


class AdminCategory(admin.ModelAdmin):
    list_display = ['name']

class AdminCustomer(admin.ModelAdmin):
    list_display= ['firstname', 'lastname', 'phone', 'email']
    
class AdminOrder(admin.ModelAdmin):
    list_display= ['product', 'customer', 'quantity', 'price', 'date']
    
admin.site.register(Product, AdminProduct)
admin.site.register(Categories, AdminCategory)
admin.site.register(Customer, AdminCustomer)
admin.site.register(Order, AdminOrder)