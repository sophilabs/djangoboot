from django import forms

from boots.models import BootVersion


class BootVersionCreationForm(forms.ModelForm):
    class Meta:
        model = BootVersion
        exclude = ('boot',)
