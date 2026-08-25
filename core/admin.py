from django.contrib import admin
from .models import Note, Homework, Task


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'user', 'created_at', 'updated_at')
    list_filter = ('subject', 'created_at', 'user')
    search_fields = ('title', 'subject', 'content', 'user__username')
    date_hierarchy = 'created_at'


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'user', 'due_date', 'completed', 'created_at')
    list_filter = ('completed', 'subject', 'due_date', 'user')
    search_fields = ('title', 'subject', 'description', 'user__username')
    date_hierarchy = 'due_date'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'due_date', 'completed', 'created_at')
    list_filter = ('completed', 'due_date', 'user')
    search_fields = ('title', 'description', 'user__username')
    date_hierarchy = 'created_at'
