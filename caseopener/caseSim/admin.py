from django.contrib import admin
from .models import Profile, Case, Skin, UserInventory

# Register your models here
admin.site.register(Case)
admin.site.register(Skin)
admin.site.register(UserInventory)

