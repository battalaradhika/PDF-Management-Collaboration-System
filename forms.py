from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PDFFile, Comment

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = PDFFile
        fields = ('name', 'file')

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if not file.name.endswith('.pdf'):
                raise forms.ValidationError("Only PDF files are allowed.")
            if file.content_type != 'application/pdf':
                raise forms.ValidationError("Uploaded file is not a valid PDF.")
        return file

class CommentForm(forms.ModelForm):
    invited_user_name = forms.CharField(required=False, label="Your Name (if not logged in)")

    class Meta:
        model = Comment
        fields = ('content', 'invited_user_name')
