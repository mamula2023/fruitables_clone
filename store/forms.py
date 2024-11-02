from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from store.models import CustomUser


# from store.models import CustomUser


class FilterForm(forms.Form):
    rangeInput = forms.IntegerField(
        label='Price',
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(
            attrs={
                'type': 'range',
                'class': 'form-range w-100',
                'oninput': "amount.value=this.value"
            }
        )
    )

    tag = forms.ChoiceField(
        label='Tags',
        widget=forms.RadioSelect,
        choices=[],  # This will be populated dynamically in the view
        required=False
    )


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control p-3',
                                               'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control p-3',
                                                'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control p-3',
                                                    'placeholder': 'Confirm Password'}),
        }

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("The two password fields didn't match.")
        return password2


class LoginForm(AuthenticationForm):  # Subclassing AuthenticationForm is optional
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control p-3',  # Add any custom class for styling
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control p-3',  # Add any custom class for styling
        'placeholder': 'Password'
    }))
