from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from projects.serializers import CryptoProjectsSerializer
from projects.models import CryptoProjects


class CryptoProjectsViewSet(ModelViewSet):
    serializer_class = CryptoProjectsSerializer
    queryset = CryptoProjects.objects.all().order_by("initial_date")
    pagination_class = PageNumberPagination