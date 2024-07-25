from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    receiver_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите имя"}
        ),
    )
    receiver_address = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите адрес"}
        ),
    )
    receiver_phone = forms.CharField(
        max_length=16,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите номер телефона"}
        ),
    )
    receiver_email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите почту"}
        )
    )
    receiver_surname = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите фамилию"}
        ),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Введите сообщение"}
        ),
        required=False
    )

    class Meta:
        model = Order
        fields = ['receiver_address', 'receiver_city', 'receiver_name', 'receiver_phone', 'receiver_email', 'receiver_surname', 'message']
