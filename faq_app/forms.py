from django import forms
from .models import FAQ

class faqFrom(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ('question', 'answer')
        labels={
            'question': 'Question',
            'answer': 'Answer',
        }
        
        widgets={
            'question': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your questions'})
        }