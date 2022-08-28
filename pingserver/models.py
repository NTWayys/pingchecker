from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class server(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, default="8.8.8.8")
    status = models.CharField(max_length=100, default="")
    notes = models.JSONField(default="Server was last down never;")
    dateadded = models.DateTimeField(
        auto_now_add=True, blank=True)
