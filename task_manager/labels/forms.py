from django import forms
from .models import Labels


class CreateLabelForm(forms.ModelForm):

    class Meta:

        model = Labels
        fields = ('name',)
