from django.db import models
from django.core.exceptions import ValidationError


class Section(models.Model):
    name = models.CharField(max_length=255)
    about = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name="categories"
        )
    name = models.CharField(max_length=255)
    about = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Criterion(models.Model):
    STATUS_CHOICES = [
        ("out_of_scope", "Out of Scope"),
        ("in_scope", "In Scope"),
        ("definition_defined", "Ausprägung definiert"),
        ("planning_review", "Review Fachplanung"),
        ("auditor_check", "Prüfung durch Auditor"),
        ("approval", "Approval"),
    ]

    prefix = models.CharField(max_length=10, default="--")
    name = models.CharField(max_length=255)
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name="criteria"
        )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="criteria"
        )
    credits = models.IntegerField(default=0)
    about = models.TextField(blank=True)
    user_story = models.TextField(blank=True)
    purpose = models.TextField(blank=True)
    problem_statement = models.TextField(blank=True)
    benefit = models.TextField(blank=True)
    functional_requirements_tier_1 = models.TextField(blank=True)
    functional_requirements_tier_2 = models.TextField(blank=True)
    functional_requirements_tier_3 = models.TextField(blank=True)
    tenant_enablement_requirements_tier_1 = models.TextField(blank=True)
    tenant_enablement_requirements_tier_2 = models.TextField(blank=True)
    tenant_enablement_requirements_tier_3 = models.TextField(blank=True)
    credit_allocation = models.TextField(blank=True)
    required_proof = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class ProjectCriterion(models.Model):
    STATUS_CHOICES = [
        ("out_of_scope", "Out of Scope"),
        ("in_scope", "In Scope"),
        ("definition_defined", "Ausprägung definiert"),
        ("planning_review", "Review Fachplanung"),
        ("auditor_check", "Prüfung durch Auditor"),
        ("approval", "Approval"),
    ]

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='project_criteria'
        )
    criterion = models.ForeignKey(
        Criterion, on_delete=models.CASCADE, related_name='project_criteria'
        )
    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default="in_scope"
    )
    note = models.TextField(blank=True)

    class Meta:
        unique_together = ('project', 'criterion')

    def clean(self):

        if ProjectCriterion.objects.filter(
            project=self.project, criterion=self.criterion
                ).exclude(pk=self.pk).exists():
            raise ValidationError(
                f"Eine ProjectCriterion mit diesem Projekt"
                f"und Kriterium {self.criterion} existiert bereits."
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project.name} - {self.criterion.name}"
