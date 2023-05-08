from django.db import models
from task_manager.dataclasses import VerboseName
from task_manager.users.models import Users
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels


class Tasks(models.Model):
    """Models for tasks"""
    name = models.CharField(max_length=150,
                            verbose_name=VerboseName.NAME.value
                            )
    description = models.CharField(max_length=1000,
                                   verbose_name=VerboseName.DESCRIPTION.value,
                                   default='')
    creator = models.ForeignKey(Users,
                                on_delete=models.PROTECT,
                                default=True,
                                blank=True
                                )
    status = models.ForeignKey(Statuses,
                               verbose_name=VerboseName.STATUS.value,
                               on_delete=models.PROTECT,
                               )
    labels = models.ManyToManyField(Labels,
                                    verbose_name=VerboseName.LABELS.value,
                                    through='TaskLabelRelation',
                                    through_fields=('task', 'label'),
                                    blank=True,
                                    )
    executor = models.ForeignKey(Users,
                                 verbose_name=VerboseName.EXECUTOR.value,
                                 on_delete=models.PROTECT,
                                 related_name='performer',
                                 )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class TaskLabelRelation(models.Model):
    """An intermediate model for man-to-many communication between tasks and
    labels. Needed to prohibit deletion of labels that are used"""
    task = models.ForeignKey(to='tasks.Tasks',
                             on_delete=models.CASCADE,
                             default=0,
                             null=True
                             )
    label = models.ForeignKey(to='labels.Labels', on_delete=models.PROTECT)
