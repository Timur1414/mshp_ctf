from django import forms


class CalcForm(forms.Form):
    expression = forms.CharField(
        label='Выражение',
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'math.sin(3+8*0.3)',
                'style': 'min-width: 400px',
            }
        )
    )
