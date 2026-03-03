from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.username


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    permission_type = models.IntegerField(default=1)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField()
    last_updated = models.DateTimeField()

    def __str__(self):
        return self.title


class EventUser(models.Model):
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.event}: {self.user}" 


class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    message = models.CharField(max_length=2000)
    created_at = models.DateTimeField()
    last_updated = models.DateTimeField()

    def __str__(self):
        return self.title


class NotificationStatus(models.Model):
    notification_status_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class NotificationUser(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    notification_status = models.ForeignKey(NotificationStatus, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return f"{self.notification}, {self.user}, {self.notification_status}"
