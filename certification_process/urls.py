from django.urls import path, include
from rest_framework_nested import routers
from .views import (
    SectionViewSet,
    CategoryViewSet,
    CriterionViewSet,
    ProjectViewSet,
    ProjectCriterionViewSet
    )

router = routers.DefaultRouter()
router.register(r'sections', SectionViewSet)
router.register(r'projects', ProjectViewSet)

sections_router = routers.NestedDefaultRouter(
    router, r'sections', lookup='section'
    )
sections_router.register(
    r'categories', CategoryViewSet, basename='section-categories'
    )

categories_router = routers.NestedDefaultRouter(
    sections_router,
    r'categories',
    lookup='category'
    )
categories_router.register(
    r'criteria', CriterionViewSet, basename='category-criteria'
    )

project_router = routers.NestedDefaultRouter(
    router, r'projects', lookup='project'
    )
project_router.register(
    r'project-criteria',
    ProjectCriterionViewSet,
    basename='project-project-criteria'
                        )

urlpatterns = [
    path('', include(router.urls)),
    path('', include(sections_router.urls)),
    path('', include(categories_router.urls)),
    path('', include(project_router.urls)),
]
