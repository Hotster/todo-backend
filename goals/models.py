from django.conf import settings
from django.db import models


class Goal(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    target_completion_date = models.DateTimeField(blank=True, null=True)
    actual_completion_date = models.DateTimeField(blank=True, null=True)
    planned_progress = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    current_progress = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    is_important = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    child_goals = models.ManyToManyField('Goal', related_name='parent_goals', blank=True)
    child_folders = models.ManyToManyField('Folder', related_name='parent_goals', blank=True)

    def __str__(self):
        return self.title


class Folder(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    important = models.BooleanField(default=False)
    child_goals = models.ManyToManyField('Goal', related_name='parent_folders', blank=True)
    child_folders = models.ManyToManyField('Folder', related_name='parent_folders', blank=True)

    def __str__(self):
        return self.name
