from django.contrib import admin
from .models import TaskModel, AttachmentModel, TaskListModel


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'created_at']


class TaskListAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'created_at']


class AttachmentAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'created_at']

    def task_title(self, obj):
        return obj.task.title if obj.task else 'No Task'

    task_title.short_description = 'Task Title'  # Label to displayed in the admin_panel

    # to make sure this field is not editable:
    def has_change_permission(self, request, obj=None):
        if obj and request.user.profile == obj.created_by:
            return True
        return False


admin.site.register(TaskListModel, TaskListAdmin)
admin.site.register(TaskModel, TaskAdmin)
admin.site.register(AttachmentModel, AttachmentAdmin)
