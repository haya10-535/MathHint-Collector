# Django フォーム
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from .models import Grade, UserProfile, Question


# ユーザー登録フォーム
class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        label='メールアドレス',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@example.com'
        })
    )

    grade = forms.ModelChoiceField(
        queryset=Grade.objects.all().order_by('order'),
        required=True,
        label='学年',
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='選択してください'
    )

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ユーザー名',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'パスワード（8文字以上）',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'パスワード（確認）',
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('このメールアドレスは既に登録されています。')
        return email

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            grade = self.cleaned_data.get('grade')
            UserProfile.objects.create(user=user, grade=grade)
        return user

# ユーザー情報編集フォーム
class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '姓',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '名',
            }),
        }


# 質問フォーム
class QuestionForm(forms.ModelForm):
    
    class Meta:
        model = Question
        fields = ['name', 'email', 'subject', 'message', 'problem_image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'お名前'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': '返信用メールアドレス'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '件名（例：二次関数の最大値問題について）'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '質問内容を詳しくご記入ください',
                'rows': 8
            }),
            'problem_image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'name': 'お名前',
            'email': '返信用メールアドレス',
            'subject': '件名',
            'message': '質問内容',
            'problem_image': '問題画像（任意）'
        }
