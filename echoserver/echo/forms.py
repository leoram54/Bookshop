from django import forms
from .models import Book, User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from argon2 import PasswordHasher, exceptions

class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Название книги'
        self.fields['author'].label = 'Автор книги'
        self.fields['price'].label = 'Цена'
    class Meta:
        model = Book
        fields = ['title', 'author', 'price']


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)
    email = forms.EmailField()
    role = forms.ChoiceField(
        label="Роль",
        choices=[
            ('user', 'Обычный пользователь'),
            ('admin', 'Админ'),
        ],
        widget=forms.RadioSelect,
        initial='user',
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        raw_password = self.cleaned_data['password1']
        ph = PasswordHasher()
        hashed_password = ph.hash(raw_password)
        user.password = hashed_password
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise forms.ValidationError("Неверное имя пользователя или пароль")
            ph = PasswordHasher()
            try:
                ph.verify(user.password, password)
            except exceptions.VerifyMismatchError:
                raise forms.ValidationError("Неверное имя пользователя или пароль")
            cleaned_data['user'] = user
        return cleaned_data

    def get_user(self):
        return self.cleaned_data.get('user')