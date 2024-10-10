from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Project, Criterion, ProjectCriterion


@receiver(post_save, sender=Project)
def create_project_criteria(sender, instance, created, **kwargs):
    if created:
        criteria = Criterion.objects.all()
        project_criteria = [
            ProjectCriterion(
                project=instance, criterion=criterion
                ) for criterion in criteria
        ]
        ProjectCriterion.objects.bulk_create(project_criteria)
