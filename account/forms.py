from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms
from django.contrib.auth.models import User
from django.forms import formset_factory

from .models import Profile, Book, Turma


class TurmaForm(forms.ModelForm):
    turma = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                           widget=forms.SelectMultiple(
                                               attrs={
                                                   'class': 'multiselect-dropdown form-control'}
                                           ))

    class Meta:
        model = Turma
        fields = ['turma']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
        'title', 'publication_date', 'author', 'price', 'pages', 'book_type',)


BookFormset = formset_factory(BookForm, extra=1)

class BookModelForm(BSModalModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
