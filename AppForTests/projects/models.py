from django.db import models
from django.db.models import URLField
from django.utils.timezone import now


class CryptoProjects(models.Model):
    name = models.CharField(max_length=200, unique=True)
    initial_date = models.DateTimeField(default=now, editable=True)
    application_link = URLField(blank=True)
    notes = models.CharField(
        max_length=100, blank=True
    )  # blank=True - field isn't required

    def __str__(self) -> str:
        return f"{self.name}"
