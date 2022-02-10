from django import forms


class DonateForm(forms.Form):
    alias = forms.CharField(max_length=50, label="Your name")
    amount = forms.DecimalField(max_digits=20, label="Donation Amount", min_value=1)
    is_anon = forms.BooleanField(label="Donate Anonymous", required=False)
    comment = forms.CharField(widget=forms.Textarea, label="Comment", required=False)
