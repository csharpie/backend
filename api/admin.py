from django.contrib import admin
from django import forms
from .models import Location, Hour, Category

admin.site.register(Location)
admin.site.register(Hour)
admin.site.register(Category)