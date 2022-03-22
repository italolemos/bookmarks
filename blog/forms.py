from django import forms
from django.contrib.auth.models import User


class TesteForm(forms.Form):
    convidados = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                                widget=forms.SelectMultiple(
                                                    attrs={
                                                        'class': 'form-control js-example-basic-multiple',
                                                        'multiple': 'multiple',
                                                        'style': 'width: 100%'}
                                                )
                                                )
