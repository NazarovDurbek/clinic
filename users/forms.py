from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from users.models import CustomUser


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control is-invalid'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control password'}))
    class Meta:
        model = CustomUser
        fields = ('email', 'password')



class UserRegistrationForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control py-4', 'placeholder':'Введите имя'}))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control py-4', 'placeholder':'Введите имя'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class':'form-control py-4', 'placeholder':'Введите Email'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control password', 'placeholder':'Введите пароль'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control c-password', 'placeholder':'Подтвердите пароль'}))

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'username', 'password1', 'password2']



class UserProfileForm(UserChangeForm):

    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control py-4'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class':'form-control py-4', 'readonly':True}))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control py-4'}), max_length=15, required=False)
    birthday = forms.DateField(widget=forms.DateInput(attrs={
        'class':'form-control py-4'}), required=False)
    gender = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control py-4'}), required=False)
    location = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control py-4'}), required=False)
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'phone', 'birthday', 'gender', 'location']

