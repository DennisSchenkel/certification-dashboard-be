# serializers.py
from rest_framework import serializers
from .models import Section, Category, Criterion


class CriterionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Criterion
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    criteria = CriterionSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = "__all__"


class SectionSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = "__all__"
