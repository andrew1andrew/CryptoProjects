from django.contrib import admin
from projects.models import CryptoProjects


@admin.register(CryptoProjects)
class CryptoProjectsAdmin(admin.ModelAdmin):
    pass
