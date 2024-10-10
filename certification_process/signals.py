# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Project, Criterion, ProjectCriterion

"""
@receiver(post_save, sender=Project)
def create_project_criteria(sender, instance, created, **kwargs):
    if created:
        all_criteria = Criterion.objects.all()
        for criterion in all_criteria:
            ProjectCriterion.objects.get_or_create(
                project=instance,
                criterion=criterion,
                defaults={'status': 'in_scope'}
            )
"""
