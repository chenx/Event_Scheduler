from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import DataStore


admin.site.register(DataStore)