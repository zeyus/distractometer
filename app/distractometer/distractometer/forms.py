from django import forms
from .models import Distraction

class DistractionForm(forms.ModelForm):
    class Meta:
        model = Distraction