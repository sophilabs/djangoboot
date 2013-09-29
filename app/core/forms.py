from django import forms

from core.validators import validate_slug


class SlugField(forms.SlugField):
    default_validators = [validate_slug]
