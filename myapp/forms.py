from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from myapp.models import Note

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',      # 👈 CSS class
                'placeholder': field.label,   # 👈 optional placeholder
            })

        self.fields['username'].help_text = "Use letters, numbers, or symbols (- _ $ @ !)"
        for field_name in self.errors:
            self.fields[field_name].widget.attrs['class'] += ' is-invalid'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=254)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',      # 👈 same CSS class
                'placeholder': field.label,
            })
        for field_name in self.errors:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs['class'] += ' is-invalid'

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter note title...',
                'class': 'note-input'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your note here...',
                'rows': 100,
                'class': 'note-textarea'
            }),
        }   