from django.db import models
from task_manager.dataclasses import VerboseName


class Statuses(models.Model):
    """Model for statuses of tasks"""
    name = models.CharField(max_length=100,
                            verbose_name=VerboseName.NAME.value)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)
