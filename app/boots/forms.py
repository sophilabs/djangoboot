from django import forms

from boots.models import BootVersion


class SearchForm(forms.Form):
    order = forms.CharField(required=False)
    page = forms.IntegerField(required=False)


class BootVersionCreationForm(forms.ModelForm):
    class Meta:
        model = BootVersion
        exclude = ('boot',)
