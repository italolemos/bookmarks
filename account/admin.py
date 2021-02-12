from django.contrib import admin
from .models import Profile, Book

admin.site.register(Book)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']
# Register your models here.
