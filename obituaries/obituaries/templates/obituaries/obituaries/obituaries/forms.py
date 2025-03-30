from django import forms
from .models import Obituary
from django.core.exceptions import ValidationError
from datetime import date

class ObituaryForm(forms.ModelForm):
    class Meta:
        model = Obituary
        fields = ['name', 'date_of_birth', 'date_of_death', 'content', 'author']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_death': forms.DateInput(attrs={'type': 'date'}),
            'content': forms.Textarea(attrs={'rows': 6}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        date_of_birth = cleaned_data.get('date_of_birth')
        date_of_death = cleaned_data.get('date_of_death')
        
        if date_of_birth and date_of_death:
            if date_of_death < date_of_birth:
                raise ValidationError("Date of death cannot be before date of birth.")
            
            if date_of_death > date.today():
                raise ValidationError("Date of death cannot be in the future.")
        
        return cleaned_data
