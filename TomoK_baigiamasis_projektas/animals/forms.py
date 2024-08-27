from .models import AnimalReview
from django import forms
from .models import Profile
from django import forms
from django.contrib.auth.models import User

class AnimalReviewForm(forms.ModelForm):
    class Meta:
        model = AnimalReview
        fields = ('content', 'animal', 'reviewer',)
        widgets = {'animal': forms.HiddenInput(), 'reviewer': forms.HiddenInput()}

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']