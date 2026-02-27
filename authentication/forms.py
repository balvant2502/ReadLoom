from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):
    
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(
        choices=[('reader', 'Reader'), ('author', 'Author')]
    )
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

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'email']
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        field_placeholders = {
            'first_name': 'Enter Full Name',
            'email': 'Enter Email'
        }

        for field_name, placeholder in field_placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({
                    'class': 'form-input',
                    'placeholder': placeholder
                })
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and self.user:
            # Check if email already exists for another user
            if CustomUser.objects.filter(email=email).exclude(id=self.user.id).exists():
                raise forms.ValidationError("This email is already registered.")
        return email
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name and self.user and first_name == self.user.first_name:
            raise forms.ValidationError("Please enter a different name.")
        return first_name
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        first_name = cleaned_data.get('first_name')
        
        if self.user:
            # Check if both email and name are the same as current
            if email == self.user.email and first_name == self.user.first_name:
                raise forms.ValidationError("Please change at least one field.")
        
        return cleaned_data
