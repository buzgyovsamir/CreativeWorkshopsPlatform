from django import forms

from .models import Workshop


class WorkshopBaseForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = (
            'title',
            'description',
            'image',
            'start_datetime',
            'end_datetime',
            'city',
            'location',
            'price',
            'capacity',
            'available_spots',
            'category',
            'tags',
        )
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter workshop title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe the workshop...',
                'rows': 4,
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'start_datetime': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'end_datetime': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter city',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter location',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'available_spots': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-select',
            }),
        }


class WorkshopCreateForm(WorkshopBaseForm):
    pass


class WorkshopEditForm(WorkshopBaseForm):
    pass


class WorkshopDeleteForm(WorkshopBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['disabled'] = True