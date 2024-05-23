from rest_framework import routers
from projects.views import CryptoProjectsViewSet

crypto_projects_router = routers.DefaultRouter()
crypto_projects_router.register("crypto_projects", viewset=CryptoProjectsViewSet, basename="crypto_projects")