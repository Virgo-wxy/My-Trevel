# -- coding: utf-8 --
from django import forms


class UserForm(forms.Form):
    user_name=forms.CharField(max_length=255)
    pwd=forms.IntegerField()
    cpwd=forms.IntegerField()
    email=forms.CharField()