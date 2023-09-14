from django.db import models
import datetime, time
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    darkmode = models.BooleanField(default=False)
    stopstart = models.IntegerField(default=0)

class ToDo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="added_by")
    date = models.DateTimeField(auto_now_add=True)
    name = models.TextField(blank = False)
    action = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user} added {self.action}"

class Alarm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="alarm_by")
    name = models.TextField(max_length=64, blank = False)
    date_time = models.DateTimeField(blank = False)
    expired = models.BooleanField(default = False)

    def __str__(self):
        return f"Alarm by {self.user} for {self.date_time}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date_time.strftime("%b %d, %Y %H:%M:%S"),
        }

class Link(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="link_by")
    date = models.DateTimeField(auto_now_add=True)
    name = models.TextField(blank = False)
    link = models.URLField()
    image = models.URLField()
    pinned = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user} added link {self.name}"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "link": self.link,
            "image":self.image
        }