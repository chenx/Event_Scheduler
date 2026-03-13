from django.db import models


class DataStore(models.Model):
    uid = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    created_at = models.DateTimeField()
 
    def __str__(self):
        return self.title
