from django import forms


class MyForms(forms.Form):
    msg = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={"class": "form-control"}
    ))
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-control"}
        )
    )
    time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={"type": "time", "class": "form-control"}
        )
    )
