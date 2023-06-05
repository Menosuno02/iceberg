from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from PIL import Image

from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)
    image = forms.ImageField(label=('Imagen'), error_messages={'invalid': (
        "Solo imágenes")}, widget=forms.FileInput, required=False)

    class Meta:
        model = Profile
        fields = ['bio', 'date_of_birth', 'sex',
                    'orientation', 'interests', 'image',]
        labels = {
            'bio': 'Biografía',
            'date_of_birth': 'Fecha de nacimiento',
            'sex': 'Sexo',
            'orientation': 'Orientación sexual',
            'interests': 'Intereses',
        }
        widgets = {
            'date_of_birth': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'})
        }

    """ Nueva imagen de usu """
    def save(self, *args, **kwargs):
        img = super(ProfileUpdateForm, self).save(*args, **kwargs)
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')
        if x and y and w and h:
            image = Image.open(img.image)
            cropped_image = image.crop((x, y, w+x, h+y))
            resized_image = cropped_image.resize((300, 300), Image.ANTIALIAS)
            resized_image.save(img.image.path)
        return img
