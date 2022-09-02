from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class server(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, default="8.8.8.8")
    statpings = models.CharField(max_length=200, default="")
    rollingpings = models.JSONField(default="Server was last down never;")
    downpings = models.JSONField(default="Server was last down never;")
    whoisdata = models.JSONField(
        default="Currently do not have whois data for this domain")
    dateadded = models.DateTimeField(
        auto_now_add=True, blank=True)
