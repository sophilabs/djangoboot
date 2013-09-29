from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from boots.models import Boot, BootVersion


class BootForm(forms.ModelForm):

    def clean(self, *args, **kwargs):
        team = self.cleaned_data.get('team')
        slug = self.cleaned_data.get('slug')
        if team and slug and Boot.objects.filter(team=team, slug=slug):
            raise ValidationError(_('A boot with the specified slug already exists for that owner.'))
        return super(BootForm, self).clean(*args, **kwargs)

    class Meta:
        model = Boot


class BootVersionForm(forms.ModelForm):

    def clean(self, *args, **kwargs):
        slug = self.cleaned_data.get('slug')
        if slug and self.boot.versions.filter(slug=slug):
            raise ValidationError(_('A version with the specified slug already exists for this boot.'))
        return super(BootVersionForm, self).clean(*args, **kwargs)

    class Meta:
        model = BootVersion
        exclude = ('boot',)
