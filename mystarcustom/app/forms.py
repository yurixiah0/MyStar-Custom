from django import forms
from django.contrib.auth.forms import UserCreationForm
from app.models import User
from django.contrib.auth import authenticate

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["name", "email", "password1", "password2"]
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスは既に登録されています")
        return email
    
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
    
    def clean(self):
        print("LoginFormのcleanが呼び出された")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        print(email, password)
        if email is None:
            raise forms.ValidationError("Eメールアドレスは必須です")
        if password is None:
            raise forms.ValidationError("パスワードは必須です")   
        self.user = authenticate(email=email, password=password)
        if self.user is None:
            raise forms.ValidationError("認証に失敗しました")
        return self.cleaned_data
    