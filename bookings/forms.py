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


class BookingCancelForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('participant', 'workshop', 'status', 'notes')
        widgets = {
            'participant': forms.TextInput(attrs={'class': 'form-control', 'disabled': True}),
            'workshop': forms.TextInput(attrs={'class': 'form-control', 'disabled': True}),
            'status': forms.TextInput(attrs={'class': 'form-control', 'disabled': True}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'disabled': True, 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['participant'].disabled = True
        self.fields['workshop'].disabled = True
        self.fields['status'].disabled = True
        self.fields['notes'].disabled = True