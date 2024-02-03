from django.contrib import admin
from .models import FootballField, ProfileUser

# Register your models here.


admin.site.register(FootballField)


class ProfileUseradmin(admin.ModelAdmin):
    list_display = ("username", "id", "email", "role")


admin.site.register(ProfileUser, ProfileUseradmin)
