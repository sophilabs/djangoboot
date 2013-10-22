from django import forms
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from haystack import forms as hsforms
from haystack.query import SearchQuerySet
from boots.models import Boot
from core.forms import FreeMultipleChoiceField


from boots.models import Boot, BootVersion


class BootForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BootForm, self).__init__(*args, **kwargs)
        self.fields['type'].choices = tuple((v, n if v != '' else 'Select a boot type',) for v, n in self.fields['type'].choices)
        self.fields['team'].label_from_instance = lambda i: i.slug

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

    def __init__(self, *args, **kwargs):
        super(BootVersionForm, self).__init__(*args, **kwargs)
        self.fields['readme'].widget.attrs['placeholder'] = _('Write some instructions...')
        self.fields['command'].widget.attrs['placeholder'] = _('./django-admin.py startproject --template=<url> <name> -or- '
                                                               'cookiecutter <url> -or-'
                                                               'pip install <package>')

    def clean(self, *args, **kwargs):
        slug = self.cleaned_data.get('slug')
        if slug:
            if self.instance and self.instance.boot_id:
                queryset = self.instance.boot.versions.exclude(id=self.instance.id)
            else:
                queryset = self.boot.versions
            queryset = queryset.filter(slug=slug)
            if queryset:
                raise ValidationError(_('A version with the specified slug already exists for this boot.'))
        return super(BootVersionForm, self).clean(*args, **kwargs)

    class Meta:
        model = BootVersion
        exclude = ('boot', 'order',)


class SearchForm(hsforms.SearchForm):

    sort = forms.CharField(required=False, label=_('Sort'))
    type = forms.CharField(required=False, label=_('Type'))
    tag = FreeMultipleChoiceField(required=False, label=_('Tag'))

    SORTS = {
        'loved': (_('Loved'), '-star_count',),
        'modified': (_('Recently Modified'), '-modified',),
        'added': (_('Recently Created'), '-created',),
        'today': (_('Today'), '-star_count_day',),
        'week': (_('Week'), '-star_count_week',),
        'month': (_('Month'), '-star_count_month',),
    }

    def __init__(self, *args, **kwargs):
        self.sort = kwargs.pop('sort', 'loved')
        self.team = kwargs.pop('team', None)
        super(SearchForm, self).__init__(*args, **kwargs)

    def search(self):
        sqs = super(SearchForm, self).search()

        sqs = sqs.facet('tags', mincount=1, limit=8)
        sqs = sqs.facet('{!ex=type_exact}type_exact', mincount=1)
        sqs = sqs.order_by(self.sorted_value, '-star_count')

        sqs = sqs.filter(flagged=False)

        if self.team:
            sqs = sqs.filter(team_slug=self.team)

        if not self.is_valid():
            return sqs
        for tag in self.tags:
            sqs = sqs.filter(tags_exact=tag)

        if self.cleaned_data['type']:
            sqs = sqs.narrow('{{!tag=type_exact}}type_exact:{0}'.format(self.cleaned_data['type']))

        return sqs

    @property
    def types(self):
        if not self.is_valid():
            return []
        return [self.cleaned_data['type']]

    @property
    def tags(self):
        if not self.is_valid():
            return []
        return self.cleaned_data['tag']

    @property
    def sorted(self):
        if self.is_valid() and self.cleaned_data['sort'] and self.cleaned_data['sort'] in self.SORTS:
            return self.cleaned_data['sort']
        else:
            return self.sort

    @property
    def sorted_name(self):
        return self.SORTS[self.sorted][0]

    @property
    def sorted_value(self):
        return self.SORTS[self.sorted][1]

    def no_query_found(self):
        return SearchQuerySet().models(Boot)
