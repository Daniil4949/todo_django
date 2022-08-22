from django.contrib import admin
from .models import Task, Profile


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'is_completed')
    list_filter = ('title',)
    prepopulated_fields = {"slug": ('title', )}


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'completed_tasks', 'uncompleted_tasks')
    list_filter = ('completed_tasks',)


admin.site.register(Task, TaskAdmin)
admin.site.register(Profile, ProfileAdmin)
# Register your models here.
