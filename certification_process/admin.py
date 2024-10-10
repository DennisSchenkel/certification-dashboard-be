
from django.contrib import admin
from .models import Project, ProjectCriterion, Section, Category, Criterion


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
    list_display = ['name', 'category', 'credits']
    list_filter = ['category']


class ProjectCriterionInline(admin.TabularInline):
    model = ProjectCriterion
    extra = 0
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
