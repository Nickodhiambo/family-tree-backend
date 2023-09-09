from django import forms
from .models import Family_Member

class MemberForm(forms.ModelForm):
    class Meta:
        model = Family_Member
        fields = ['first_name', 'last_name', 'parent']
