from django import forms
from django.core.validators import FileExtensionValidator
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "p-2",
                "placeholder": "Joe",
                "autofocus": True,
                "autocapitalize": "none",
                "autocomplete": "username",
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "p-2 input-field",
                "placeholder": "Abcd133",
            }
        ),
    )


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "p-2",
                "placeholder": "Email",
                "autofocus": True,
                "autocomplete": "email",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "p-2",
                    "placeholder": "Username",
                    "autofocus": True,
                    "autocapitalize": "none",
                    "autocomplete": "username",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs["placeholder"] = "Password"
        self.fields["password1"].widget.attrs["class"] = "p-2"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm Password"
        self.fields["password2"].widget.attrs["class"] = "p-2"