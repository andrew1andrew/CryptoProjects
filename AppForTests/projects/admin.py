from django.contrib import admin
from .models import CryptoProjects


@admin.register(CryptoProjects)
class CryptoProjectsAdmin(admin.ModelAdmin):
    pass
