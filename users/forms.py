from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

Hostel = (
    ('Push_9', 'Pushkina, 32'),
    ('Push_8', 'Pushkina, 32a'),
)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50, required=True, label='Имя')
    last_name = forms.CharField(max_length=50, required=True, label='Фамилия')
    hostel = forms.ChoiceField(choices = Hostel)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'hostel']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']