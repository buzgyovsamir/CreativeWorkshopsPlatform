from django import forms

from bookings.models import Booking


class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('notes',)
        widgets = {
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Optional notes...',
                'rows': 4,
            }),
        }
        labels = {
            'notes': 'Notes',
        }
        help_texts = {
            'notes': 'Optional field.',
        }


class BookingCancelForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label='I confirm that I want to cancel this booking.',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )