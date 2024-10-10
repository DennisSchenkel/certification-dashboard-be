from django.contrib import admin
from .models import Project, ProjectCriterion, Section, Category, Criterion
from django import forms
from django.core.exceptions import ValidationError


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


class CriterionInline(admin.TabularInline):
    model = Criterion
    extra = 1


class SectionAdmin(admin.ModelAdmin):
    inlines = [CategoryInline]
    list_display = ['name', 'about']


class CategoryAdmin(admin.ModelAdmin):
    inlines = [CriterionInline]
    list_display = ['name', 'section', 'about']
    list_filter = ['section']


class CriterionAdmin(admin.ModelAdmin):
    list_display = ['prefix', 'name', 'category']
    list_filter = ['category']


class ProjectCriterionInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        seen_criteria = set()
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get(
                'DELETE', False
                    ):
                criterion = form.cleaned_data.get('criterion')
                if criterion in seen_criteria:
                    raise ValidationError(
                        f"Doppeltes Kriterium: {criterion.name}"
                        )
                seen_criteria.add(criterion)


class ProjectCriterionInline(admin.TabularInline):
    model = ProjectCriterion
    formset = ProjectCriterionInlineFormSet
    extra = 1
    readonly_fields = ['credits']
    fields = ['criterion', 'credits', 'status', 'note']

    def credits(self, obj):
        return obj.criterion.credits
    credits.short_description = 'Credits'


class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectCriterionInline]
    list_display = ['name']


admin.site.register(Section, SectionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Criterion, CriterionAdmin)
admin.site.register(Project, ProjectAdmin)
