from django.db import models
from django.forms import ModelChoiceField
from django_earthdistance.models import EarthDistanceQuerySet

class Category(models.Model):
    name = models.CharField(max_length=200, blank=False)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ('name', )

    def __str__(self): 
        return self.name

class Location(models.Model):
    objects = EarthDistanceQuerySet.as_manager()

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False)
    address_1 = models.CharField(max_length=200, blank=False)
    address_2 = models.CharField(max_length=200, blank=True, default='')
    city = models.CharField(max_length=30, blank=False)
    state = models.CharField(max_length=2, blank=True, default='PA')
    zipcode = models.CharField(max_length=5, blank=False)
    phone = models.CharField(max_length=20, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    category = models.ForeignKey(Category)
    description = models.TextField(blank=True, default='')
    website = models.URLField(max_length=200, blank=True, default='')
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('name', )

    def __str__(self): 
        return self.name

class Day(models.Model):
    description = models.CharField(blank=False, max_length=100)
    sort_order = models.IntegerField(blank=False, default=1)

    class Meta:
        ordering = ('sort_order', )

    def __str__(self): 
        return self.description

class Hour(models.Model):
    location = models.ForeignKey(
        Location, related_name='hours', on_delete=models.CASCADE)
    day = models.ForeignKey(Day)
    open_time = models.TimeField(blank=False)
    close_time = models.TimeField(blank=False)

    class Meta:
        ordering = ('location', )

    def __str__(self):
        return self.location.name + " - " + self.day.description + " - " + self.open_time.strftime("%H:%M") + " - " + self.close_time.strftime("%H:%M")
