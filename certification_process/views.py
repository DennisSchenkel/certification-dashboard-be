from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Section, Category, Criterion, Project, ProjectCriterion
from .serializers import (
    SectionSerializer,
    CategorySerializer,
    CriterionSerializer,
    ProjectSerializer,
    ProjectCriterionSerializer,
)
import logging

logger = logging.getLogger(__name__)


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.AllowAny]


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        section_id = self.kwargs.get("section_pk")
        logger.debug(f"Filtering categories for section_id: {section_id}")
        return Category.objects.filter(section_id=section_id)


class CriterionViewSet(viewsets.ModelViewSet):
    serializer_class = CriterionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # `category_pk` wird durch den verschachtelten Router bereitgestellt
        category_id = self.kwargs.get("category_pk")
        logger.debug(f"Filtering criteria for category_id: {category_id}")
        return Criterion.objects.filter(category_id=category_id)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]

    @action(
        detail=True,
        methods=["get", "post"],
        url_path="criteria/(?P<criterion_id>[^/.]+)/result",
        url_name="criterion-result",
    )
    def criterion_result(self, request, pk=None, criterion_id=None):
        project = self.get_object()

        if request.method == "GET":
            # Abrufen des spezifischen ProjectCriterion-Objekts
            project_criterion = ProjectCriterion.objects.filter(
                project=project, criterion_id=criterion_id
            ).first()

            if not project_criterion:
                return Response(
                    {"detail": "ProjectCriterion not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = ProjectCriterionSerializer(project_criterion)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == "POST":
            serializer = ProjectCriterionSerializer(data=request.data)
            if serializer.is_valid():
                project_criterion,
                created = ProjectCriterion.objects.update_or_create(
                    project=project,
                    criterion_id=criterion_id,
                    defaults={
                        "status": serializer.validated_data.get("status", "in_scope"),
                        "note": serializer.validated_data.get("note", ""),
                    },
                )
                response_serializer = ProjectCriterionSerializer(project_criterion)
                if created:
                    return Response(
                        response_serializer.data, status=status.HTTP_201_CREATED
                    )
                else:
                    return Response(response_serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectCriterionViewSet(viewsets.ModelViewSet):
    queryset = ProjectCriterion.objects.all()
    serializer_class = ProjectCriterionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = ProjectCriterion.objects.all()
        project_id = self.request.query_params.get("project_id")
        if project_id is not None:
            queryset = queryset.filter(project__id=project_id)
        return queryset

    def perform_update(self, serializer):
        serializer.save()
