# forms.py
from django import forms

# ... (ProjectileMotionForm remains the same) ...

class ProjectileMotionForm(forms.Form):
    initial_velocity = forms.FloatField(
        label='Initial Velocity (m/s)',
        min_value=0.1,
        widget=forms.NumberInput(attrs={
            'class': 'w-full p-2 border rounded mb-2',
            'placeholder': 'e.g., 50'
        })
    )
    angle = forms.FloatField(
        label='Angle (degrees)',
        min_value=-90, # Changed to allow downward throws
        max_value=90,
        widget=forms.NumberInput(attrs={
            'class': 'w-full p-2 border rounded mb-2',
            'placeholder': 'e.g., 45'
        })
    )
    initial_height = forms.FloatField(
        label='Initial Height (m)',
        required=False,
        initial=0,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'w-full p-2 border rounded mb-2',
            'placeholder': 'Optional (default 0)'
        })
    )
    # final_height = forms.FloatField(
    #     label='Target/Final Height (m)',
    #     required=False,
    #     initial=0,
    #     min_value=0,
    #     widget=forms.NumberInput(attrs={
    #         'class': 'w-full p-2 border rounded mb-2',
    #         'placeholder': 'Optional (default 0)'
    #     })
    # )

class PracticeAnswerForm(forms.Form):
    """Dynamic form that generates fields for all questions in a level"""
    
    def __init__(self, *args, **kwargs):
        # Extract custom question data from kwargs
        questions_data = kwargs.pop('questions_data', [])
        super().__init__(*args, **kwargs)
        
        # Dynamically create a field for each question
        for q_data in questions_data:
            field_name = f"answer_{q_data['type']}"
            self.fields[field_name] = forms.IntegerField(
                label=f"{q_data['text']} ({q_data['unit']})",
                required=True,
                widget=forms.NumberInput(attrs={
                    'class': 'w-full text-xl font-mono text-center bg-gray-900 text-green-400 border-2 border-green-600 rounded p-3 focus:outline-none focus:border-green-400',
                    'placeholder': f'Enter integer ({q_data["unit"]})',
                    'step': '1'
                })
            )