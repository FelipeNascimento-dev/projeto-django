from django.contrib import admin
from .models import Sale

@admin.register(Sale)

class SaleAdmin(admin.ModelAdmin):
    list_display = ('date', 'product', 'quantity', 'price') 