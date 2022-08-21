from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_completed')
    list_filter = ('title',)
    prepopulated_fields = {"slug": ('title', )}


admin.site.register(Task, TaskAdmin)

# Register your models here.
