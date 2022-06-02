from django import forms


class MyForms(forms.Form):
    msg = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={"class": "form-control"}
    ))

    date_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"class": "form-control", "type": "datetime-local"}
        )
    )
