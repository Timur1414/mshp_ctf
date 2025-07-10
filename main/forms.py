from django import forms
from main.models import Note


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


class CreateNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'text', 'is_open', 'author']
        labels = {
            'title': 'Заголовок заметки',
            'text': 'Текст заметки',
            'is_open': 'Публичная',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'is_open': forms.CheckboxInput(),
            'author': forms.HiddenInput(),
        }


class FindNoteForm(forms.Form):
    text = forms.CharField(
        label='Текст',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )
