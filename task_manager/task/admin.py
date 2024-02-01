from django.contrib import admin
from .models import Task, TaskLabelRelation


class TaskLabelRelationInline(admin.TabularInline):
    model = TaskLabelRelation
    extra = 1


class TaskAdmin(admin.ModelAdmin):
    inlines = [TaskLabelRelationInline]


admin.site.register(Task, TaskAdmin)
