from django import forms
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from haystack import forms as hsforms
from haystack.query import SearchQuerySet
from boots.models import Boot
from core.forms import FreeMultipleChoiceField


from boots.models import Boot, BootVersion


class BootForm(forms.ModelForm):

    def clean(self, *args, **kwargs):
        team = self.cleaned_data.get('team')
        slug = self.cleaned_data.get('slug')
        if team and slug:
            queryset = Boot.objects.filter(team=team, slug=slug)
            if self.instance:
                queryset = queryset.exclude(id=self.instance.id)
            if queryset:
                raise ValidationError(_('A boot with the specified slug already exists for that owner.'))
        return super(BootForm, self).clean(*args, **kwargs)

    class Meta:
        model = Boot


class BootVersionForm(forms.ModelForm):

    def clean(self, *args, **kwargs):
        slug = self.cleaned_data.get('slug')
        if slug:
            queryset = self.boot.versions.filter(slug=slug)
            if self.instance:
                queryset = queryset.exclude(id=self.instance.id)
            if queryset:
                raise ValidationError(_('A version with the specified slug already exists for this boot.'))
        return super(BootVersionForm, self).clean(*args, **kwargs)

    class Meta:
        model = BootVersion
        exclude = ('boot',)


class SearchForm(hsforms.SearchForm):

    #sort = forms.CharField(required=False, label=_('Sort'))

    type = forms.CharField(required=False, label=_('Type'))
    tag = FreeMultipleChoiceField(required=False, label=_('Tag'))

    def search(self):
        sqs = super(SearchForm, self).search()

        sqs = sqs.facet('tags')

        if not self.is_valid():
            return sqs
        if self.cleaned_data['tag']:
            for tag in self.cleaned_data['tag']:
                sqs = sqs.filter(tags_exact=tag)
        if self.cleaned_data['type']:
            sqs = sqs.filter(type_exact=self.cleaned_data['type'])

        return sqs

    def no_query_found(self):
        return SearchQuerySet().models(Boot)
