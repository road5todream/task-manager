from .models import Tasks
from django import forms


class CreateTaskForm(forms.ModelForm):

    class Meta:

        model = Tasks
        fields = ('name',
                  'description',
                  'status',
                  'creator',
                  'executor',
                  'labels'
                  )
        widgets = {
            'description': forms.Textarea(),
            'creator': forms.HiddenInput(),
            'labels': forms.SelectMultiple(
                attrs={'multiple': ''}
            )
        }
