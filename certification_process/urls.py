from django.urls import path, include
from rest_framework import routers
from .views import SectionViewSet, CategoryViewSet, CriterionViewSet

router = routers.DefaultRouter()
router.register(r"sections", SectionViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"criteria", CriterionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
