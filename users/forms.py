from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'style':'outline:none;'},))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'style':'outline:none;',}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'style':'outline:none;',}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'style':'outline:none;',}))

    class Meta: # A metaclass. 'Meta' is just user-defined class name
        model = User
        fields = ("email", "username", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
      