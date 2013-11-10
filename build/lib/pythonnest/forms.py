from django import forms

__author__ = 'flanker'


class RegisterForm(forms.Form):
    name = forms.CharField(min_length=0, max_length=255, required=False, initial='')
    author = forms.CharField(min_length=0, max_length=255, required=False, initial='')
    author_email = forms.CharField(min_length=0, max_length=255, required=False, initial='')
    description = forms.CharField(required=False)
    version = forms.CharField(min_length=0, max_length=50, required=False)
    license = forms.CharField(min_length=0, max_length=255, required=False, initial='UNKNOWN')
    home_page = forms.CharField(min_length=0, max_length=255, required=False, initial='')
    metadata_version = forms.FloatField(initial=1.0)
    download_url = forms.CharField(min_length=0, max_length=255, required=False, initial='UNKNOWN')
    summary = forms.CharField(min_length=0, max_length=255, required=False, initial='')
    platform = forms.CharField(min_length=0, max_length=50, required=False, initial='UNKNOWN')
