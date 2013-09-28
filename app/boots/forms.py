from django import forms


class SearchForm(forms.Form):

    order = forms.CharField(required=False)
    page = forms.IntegerField(required=False)