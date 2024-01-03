from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Importando AuthenticationForm Padrão para sobrescrever com função super
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=None, *args, **kwargs)
        self.fields['username'].widget.attrs.update({"class": "form-control"})
        self.fields['password'].widget.attrs.update({"class": "form-control"})

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=3,
        label="Primeiro Nome",
        widget = forms.TextInput(attrs={"class": "form-control"})
    )

    last_name = forms.CharField(
        required=True,
        min_length=3,
        label="Sobrenome",
        widget = forms.TextInput(attrs={"class": "form-control"})
    )

    email = forms.EmailField(
        label="Email",
        widget = forms.TextInput(attrs={"class": "form-control"})
    )

    username = forms.CharField(
        label="Nome de Usuário",
        widget = forms.TextInput(attrs={"class": "form-control"})
    )

    password1 = forms.CharField(
        strip=False,
        label="Senha",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password","class": "form-control"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label="Confirme sua Senha",
        widget = forms.PasswordInput(attrs={"class": "form-control"})
    )
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username', 'password1', 'password2',
        )        

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('Já existe este e-mail', code='invalid')
            )

        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                )

        return password1

class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        error_messages={
            'min_length': 'Please, add more than 2 letters.'
        },
        widget = forms.TextInput(attrs={"class": "form-control"})
    )

    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        widget = forms.TextInput(attrs={"class": "form-control"})
    )

    email = forms.EmailField(
        widget = forms.TextInput(attrs={"class": "form-control"})
    )

    username = forms.CharField(
        widget = forms.TextInput(attrs={"class": "form-control"})
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False
    )

    password2 = forms.CharField(
        label="Password 2",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control"}),
        required=False
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username',
        )

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        password = cleaned_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('Senhas não batem')
                )

        return super().clean()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError('Já existe este e-mail', code='invalid')
                )

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                )

        return password1
    
class PasswordUpdateForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False
    )

    password2 = forms.CharField(
        label="Alterar Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control"}),
        required=False
    )

    class Meta:
        model = User
        fields = (
            'password1', 'password2',
        )

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        password = cleaned_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                )

        return password1

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('Senhas não batem')
                )

        return super().clean()