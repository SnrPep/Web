from django import forms

class FeedbackForm(forms.Form):
    name = forms.CharField(
        label="Имя",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваше имя',
            'required': True  # Поле обязательно
        })
    )
    phone = forms.CharField(
        label="Телефон",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7 XXX XX XX XX',
            'pattern': r'\+7 \d{3} \d{2} \d{2} \d{2}',
            'title': 'Формат телефона: +7 XXX XX XX XX',
            'required': True  # Поле обязательно
        })
    )
    message = forms.CharField(
        label="Текст сообщения",
        max_length=200,
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