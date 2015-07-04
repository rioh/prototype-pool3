from django.db import models


class ContactInformation(models.Model):
    """
    Model corresponding to Contact Us form fields
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    contact_name = models.CharField(max_length=100, null=False, blank=False)
    contact_email = models.EmailField(max_length=200, null=False, blank=False)
    contact_comment = models.TextField(null=False, blank=False)