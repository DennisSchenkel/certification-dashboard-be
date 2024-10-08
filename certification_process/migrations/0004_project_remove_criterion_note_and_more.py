# Generated by Django 5.1.1 on 2024-10-09 17:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("certification_process", "0003_criterion_note"),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="criterion",
            name="note",
        ),
        migrations.RemoveField(
            model_name="criterion",
            name="status",
        ),
        migrations.CreateModel(
            name="ProjectCriterion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("out_of_scope", "Out of Scope"),
                            ("in_scope", "In Scope"),
                            ("definition_defined", "Ausprägung definiert"),
                            ("planning_review", "Review Fachplanung"),
                            ("auditor_check", "Prüfung durch Auditor"),
                            ("approval", "Approval"),
                        ],
                        default="in_scope",
                        max_length=25,
                    ),
                ),
                ("note", models.TextField(blank=True)),
                (
                    "criterion",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="project_criteria",
                        to="certification_process.criterion",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="project_criteria",
                        to="certification_process.project",
                    ),
                ),
            ],
            options={
                "unique_together": {("project", "criterion")},
            },
        ),
    ]
