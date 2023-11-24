from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django import forms
from .models import Request, AdditionalImage, User, Category
from django.forms import inlineformset_factory


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Пароль (повторно)', widget=forms.PasswordInput)
    last_name = forms.CharField(label='Фамилия', max_length=200, widget=forms.TextInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label='Имя', max_length=200, widget=forms.TextInput(attrs={'class': 'form-input'}))
    patronymic = forms.CharField(label='Отчество', max_length=200, widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'patronymic', 'username', 'email', 'password1', 'password2', 'send_messages')

    # def clean_password1(self):
    #     password1 = self.cleaned_data['password1']
    #     if password1:
    #         password_validation.validate_password(password1)
    #     return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                'Введенные пароли не совпадают', code='password_mismatch'
            )}
            raise ValidationError(errors)


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        return user

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalpha():
            raise forms.ValidationError("Фамилия должно состоять только из букв")
        return last_name

    def clean_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            raise forms.ValidationError("Имя должно состоять только из букв")
        return first_name

    def clean_patronymic(self):
        patronymic = self.cleaned_data['patronymic']
        if not patronymic.isalpha():
            raise forms.ValidationError("Отчество должно состоять только из букв")
        return patronymic

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return email

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class RequestForm(forms.ModelForm):
   class Meta:
       model = Request
       fields = ['title', 'content', 'category', 'image']
       # widgets = {'author': forms.HiddenInput}

       def clean_image(self):
           image = self.cleaned_data.get('image')
           if image:
               if image.size > 2 * 1024 * 1024:
                   raise forms.ValidationError("Изображение превышает 2 Мб")
           return image

AIFormSet = inlineformset_factory(Request, AdditionalImage, fields='__all__')


class CategoryForm(forms.ModelForm):
   class Meta:
       model = Category
       fields = ['category_title']


class RequestStatusCompleted(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['image_design']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Изображение превышает 2 Мб")
        return image

class RequestStatusAcceptWork(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['comment']