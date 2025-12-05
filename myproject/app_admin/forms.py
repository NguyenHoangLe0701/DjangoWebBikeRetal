from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re
from .models import CustomUser

# Validator cho số điện thoại Việt Nam
phone_validator = RegexValidator(
    regex=r'^[0-9]{10,11}$',
    message='Số điện thoại phải có 10-11 chữ số'
)

# Form đăng ký
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email của bạn',
            'autocomplete': 'email'
        }),
        help_text='Nhập địa chỉ email hợp lệ'
    )
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        validators=[phone_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Số điện thoại (10-11 số)',
            'pattern': '[0-9]{10,11}',
            'autocomplete': 'tel'
        }),
        help_text='Số điện thoại phải có 10-11 chữ số'
    )
    full_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Họ và tên đầy đủ',
            'autocomplete': 'name'
        })
    )
    password1 = forms.CharField(
        label='Mật khẩu',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mật khẩu (tối thiểu 8 ký tự)',
            'autocomplete': 'new-password'
        }),
        help_text='Mật khẩu phải có ít nhất 8 ký tự, bao gồm chữ hoa, chữ thường, số và ký tự đặc biệt'
    )
    password2 = forms.CharField(
        label='Xác nhận mật khẩu',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Xác nhận mật khẩu',
            'autocomplete': 'new-password'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'full_name', 'password1', 'password2')

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            # Kiểm tra độ dài
            if len(password1) < 8:
                raise ValidationError("Mật khẩu phải có ít nhất 8 ký tự.")
            
            # Kiểm tra có chữ hoa
            if not re.search(r'[A-Z]', password1):
                raise ValidationError("Mật khẩu phải có ít nhất một chữ cái viết hoa.")
            
            # Kiểm tra có chữ thường
            if not re.search(r'[a-z]', password1):
                raise ValidationError("Mật khẩu phải có ít nhất một chữ cái viết thường.")
            
            # Kiểm tra có số
            if not re.search(r'[0-9]', password1):
                raise ValidationError("Mật khẩu phải có ít nhất một chữ số.")
            
            # Kiểm tra có ký tự đặc biệt
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
                raise ValidationError("Mật khẩu phải có ít nhất một ký tự đặc biệt (!@#$%^&*...).")
        
        return password1

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            # Kiểm tra username không chứa ký tự đặc biệt
            if not re.match(r'^[a-zA-Z0-9_]+$', username):
                raise ValidationError("Tên đăng nhập chỉ được chứa chữ cái, số và dấu gạch dưới.")
            if len(username) < 3:
                raise ValidationError("Tên đăng nhập phải có ít nhất 3 ký tự.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        user.full_name = self.cleaned_data['full_name']
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Kiểm tra format email
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, email):
                raise ValidationError("Địa chỉ email không hợp lệ.")
            
            if CustomUser.objects.filter(email=email).exists():
                raise ValidationError("Email này đã được sử dụng.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            # Loại bỏ khoảng trắng và ký tự đặc biệt
            phone_number = re.sub(r'[^\d]', '', phone_number)
            
            # Kiểm tra độ dài
            if len(phone_number) < 10 or len(phone_number) > 11:
                raise ValidationError("Số điện thoại phải có 10-11 chữ số.")
            
            if CustomUser.objects.filter(phone_number=phone_number).exists():
                raise ValidationError("Số điện thoại này đã được sử dụng.")
        return phone_number

# Form đăng nhập
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email hoặc số điện thoại'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mật khẩu'})
    )

# Form lấy lại mật khẩu
class ForgotPasswordForm(forms.Form):
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Nhập số điện thoại'}))