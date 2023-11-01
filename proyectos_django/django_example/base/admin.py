from django.contrib import admin
from .models import Country, City, Municipality, State, Parish

admin.site.register(State)
admin.site.register(Parish)