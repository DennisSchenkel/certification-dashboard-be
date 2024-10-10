from rest_framework import serializers
from .models import Section, Category, Criterion, Project, ProjectCriterion


class CriterionSerializer(serializers.ModelSerializer):
    section_id = serializers.IntegerField(
        source='section.id', read_only=True
        )
    section_name = serializers.CharField(
        source='section.name', read_only=True
        )

    # Inkludiere category_id und category_name
    category_id = serializers.IntegerField(
        source='category.id', read_only=True
        )
    category_name = serializers.CharField(
        source='category.name', read_only=True
        )

    class Meta:
        model = Criterion
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    criteria = CriterionSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'about', 'section', 'criteria']


class SectionSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'name', 'about', 'categories']


class ProjectCriterionSerializer(serializers.ModelSerializer):
    criterion = CriterionSerializer(read_only=True)
    status_display = serializers.CharField(
        source='get_status_display', read_only=True
    )

    class Meta:
        model = ProjectCriterion
        fields = ['id', 'criterion', 'status', 'status_display', 'note']
        read_only_fields = ['id', 'criterion', 'status_display']

    def validate_status(self, value):
        if value not in dict(ProjectCriterion.STATUS_CHOICES):
            raise serializers.ValidationError("Ungültiger Status.")
        return value


class ProjectSerializer(serializers.ModelSerializer):
    project_criteria = ProjectCriterionSerializer(many=True, read_only=True)
    total_credits = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'project_criteria', 'total_credits'
            ]

    def get_total_credits(self, obj):
        return obj.total_credits()
