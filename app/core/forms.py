from django import forms

from core.validators import validate_slug, validate_non_reserved


class SlugField(forms.SlugField):
    default_validators = [validate_slug, validate_non_reserved]


class FreeMultipleChoiceField(forms.MultipleChoiceField):

    widget = forms.MultipleHiddenInput

    def valid_value(self, value):
        return True