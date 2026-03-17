from django import forms


class LemmatizerInputForm(forms.Form):
    text = forms.CharField(
        label="Формы для лемматизации",
        max_length=4000,
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "placeholder": "Например: тарпыдинзь, тарпыдась, тарпывась, тарпыми’. Разделители: пробел или новая строка.",
            }
        ),
    )

    def clean_text(self):
        return (self.cleaned_data.get("text") or "").strip()
