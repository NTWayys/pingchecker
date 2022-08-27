from django.db import models
from django.contrib.auth.models import User
from django_q.models import Schedule
# Create your models here.


class server(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, default="8.8.8.8")
    status = models.CharField(max_length=100, default="")
    notes = models.JSONField(default="Server was last down never")


Schedule.objects.create(
    func='pingserver.utils.updateServerStatus',  # module and func to run
    schedule_type=Schedule.MINUTES,
    minutes=1,  # run every minute
    repeats=-1  # keep repeating, repeat forever
)
