from django import forms
from .models import Incident


class IncidentForm(forms.ModelForm):

    class Meta:
        model = Incident

        fields = [
            'title',
            'description',
            'category',
            'priority'
        ]

        widgets = {

            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter incident title'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Describe the issue...'
                }
            ),

            'category': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Network / Hardware / Software / Security / Other'
                }
            ),

            'priority': forms.Select(
                choices=[
                    ('Low', 'Low'),
                    ('Medium', 'Medium'),
                    ('High', 'High'),
                    ('Critical', 'Critical')
                ],
                attrs={
                    'class': 'form-select'
                }
            ),
        }