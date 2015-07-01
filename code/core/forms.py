from django import forms
from core.models import ContactInformation


class ContactInformationForm(forms.ModelForm):
    """
    Capture all fields for this form with the exclusion of server-side timestamp
    """
    class Meta:
        model = ContactInformation
        exclude = ('timestamp',)
