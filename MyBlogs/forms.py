from django import forms
from User.models import Blog

class Blog_create(forms.Form):
    title = forms.CharField(max_length=60)
    content = forms.CharField(widget=forms.Textarea)

class Blog_update(forms.Form):
    title = forms.CharField(max_length=60)
    content =forms.CharField(widget=forms.Textarea)

