from django import forms
from phonenumber_field.formfields import PhoneNumberField

class FeedbackForm(forms.Form):
    name = forms.CharField(
        label="Имя",
        max_length=100,
        min_length=1,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваше имя',
            'required': True  # Поле обязательно
        })
    )
    phone = PhoneNumberField()
    message = forms.CharField(
        label="Текст сообщения",
        max_length=200,
        min_length=10,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Ваше сообщение (макс. 200 символов)',
            'required': True  # Поле обязательно
        })
    )
    privacy_policy = forms.BooleanField(
        label='Я ознакомлен с <a href="/privacy-policy.pdf" target="_blank">политикой конфиденциальности</a>',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': True})  # Поле обязательно
    )