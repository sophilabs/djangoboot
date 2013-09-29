from django import forms

from core.validators import validate_slug


class SlugField(forms.SlugField):
    default_validators = [validate_slug]


class FreeMultipleChoiceField(forms.MultipleChoiceField):

    widget = forms.MultipleHiddenInput

    def valid_value(self, value):
        return True