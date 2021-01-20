import datetime
from django.db import models
from django.utils import timezone




class Board(models.Model):
    title = models.CharField(max_length=100)
    context = models.CharField(max_length=1000)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
