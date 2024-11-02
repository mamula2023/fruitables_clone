from django import forms

class FilterForm(forms.Form):
    rangeInput = forms.IntegerField(
        label='Price',
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(
            attrs={
                'type': 'range',
                'class': 'form-range w-100',
                'oninput': "amount.value=this.value"
            }
        )
    )

    tag = forms.ChoiceField(
        label='Tags',
        widget=forms.RadioSelect,
        choices=[],  # This will be populated dynamically in the view
        required=False
    )
