from .models import Tasks
import django_filters
from task_manager.statuses.models import Statuses
from task_manager.users.models import Users
from task_manager.labels.models import Labels
from django.utils.translation import gettext as _
from django import forms


class TaskFilter(django_filters.FilterSet):

    def self_widget_filter(self, queryset, name, value):
        if value:
            author = getattr(self.request, 'user', None)
            if author:
                return queryset.filter(creator=author)
            return queryset.none()
        return queryset

    status = django_filters.ModelChoiceFilter(
        queryset=Statuses.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select',
        }))
    executor = django_filters.ModelChoiceFilter(
        queryset=Users.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select',
        }))
    labels = django_filters.ModelChoiceFilter(
        label=_('Label'),
        queryset=Labels.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
    self_task = django_filters.BooleanFilter(
        label=_('Only their tasks'),
        method='self_widget_filter',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }))

    class Meta:

        model = Tasks
        fields = (
            'status',
            'executor',
            'labels',
        )
