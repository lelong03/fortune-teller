from django import forms

class FutureInputForm(forms.Form):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
