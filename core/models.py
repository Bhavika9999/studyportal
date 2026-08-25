from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Note(models.Model):
    """
    Model representing academic lecture and study notes created by a student.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} ({self.subject})"


class Homework(models.Model):
    """
    Model representing academic assignments, practicals, and homework.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='homeworks')
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['completed', 'due_date', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.subject} (Due: {self.due_date})"

    @property
    def is_overdue(self):
        """Check if homework is past its due date and not completed."""
        if not self.completed and self.due_date < timezone.now().date():
            return True
        return False


class Task(models.Model):
    """
    Model representing a student's daily study tasks and to-do items.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['completed', 'due_date', '-created_at']

    def __str__(self):
        return f"{self.title} - {'Done' if self.completed else 'Pending'}"

    @property
    def is_overdue(self):
        """Check if task is past its due date and not completed."""
        if not self.completed and self.due_date and self.due_date < timezone.now().date():
            return True
        return False
