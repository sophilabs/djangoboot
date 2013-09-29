from django import forms
from django.utils.translation import ugettext as _
from haystack import forms as hsforms
from haystack.query import SearchQuerySet
from boots.models import Boot

from boots.models import BootVersion


class BootVersionCreationForm(forms.ModelForm):
    class Meta:
        model = BootVersion
        exclude = ('boot',)


class SearchForm(hsforms.SearchForm):

    type = forms.CharField(required=False, label=_('Type'))

    def search(self):
        sqs = super(SearchForm, self).search()
        if not self.is_valid():
            return sqs
        if self.cleaned_data['type']:
            sqs = sqs.filter_and(type=self.cleaned_data['type'])
        return sqs

    def no_query_found(self):
        return SearchQuerySet().models(Boot)