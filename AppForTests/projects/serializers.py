from rest_framework import serializers
from projects.models import CryptoProjects


class CryptoProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoProjects
        fields = ['id', 'name', 'initial_date', 'application_link', 'notes']