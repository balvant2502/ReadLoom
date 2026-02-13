from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):
    
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name','email','password1', 'password2', 'user_type'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
        field_placeholders = {
            'first_name': 'Enter Full Name',
            'email': 'Enter Email',
            'password1': 'Enter Password',
            'password2': 'Confirm Password',
            'user_type': 'Select Account Type'
        }

        for field_name, placeholder in field_placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({
                    'class': 'form-input',
                    'placeholder': placeholder
                })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    def save(self, commit=True):
        user = super().save(commit=False)

        # Set username automatically from email
        user.username = user.first_name

        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-input',
                'placeholder': field.label
            })