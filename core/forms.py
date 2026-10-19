from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["name", "rating", "text"]

        labels = {
            "name": "Ваше имя",
            "rating": "Оценка",
            "text": "Ваш отзыв",
        }

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Введите ваше имя",
            }),
            # "rating": forms.Select(
            #     choices=[(i, f"{i}/5") for i in range(5, 0, -1)]
            # ),
            "text": forms.Textarea(attrs={
                "placeholder": "Поделитесь впечатлениями...",
                "rows": 4,
            }),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["text"].required = False

    def clean_rating(self):
        rating = self.cleaned_data["rating"]

        if not 1 <= rating <= 5:
            raise forms.ValidationError("Оценка должна быть от 1 до 5.")

        return rating