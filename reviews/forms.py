from django import forms

from reviews.models import Review


class ReviewBaseForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5,
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share your experience...',
                'rows': 4,
            }),
        }
        labels = {
            'rating': 'Rating',
            'comment': 'Comment',
        }
        help_texts = {
            'rating': 'Choose a rating from 1 to 5.',
        }


class ReviewCreateForm(ReviewBaseForm):
    pass


class ReviewEditForm(ReviewBaseForm):
    pass


class ReviewDeleteForm(ReviewBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['disabled'] = True
            field.disabled = True