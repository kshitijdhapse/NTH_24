from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
import math

# Create your models here.

class User(AbstractUser):
    current_level = models.PositiveIntegerField(default=1)
    hidden_on_leaderboard = models.BooleanField(default=False)
    phone = models.IntegerField(null = True)
    last_level_updated_time = models.DateTimeField(auto_now=True)
    college = models.CharField(max_length=500,null = True)
    promo_used = models.BooleanField(default=False)
    is_rigged = models.BooleanField(default=False)
    machine_used = models.IntegerField(default=0)
    # Currency
    paidHintTaken = models.BooleanField(default=False)
    keys = models.PositiveIntegerField(default = 2)


    REQUIRED_FIELDS = ['phone', 'first_name', 'last_name', 'email', 'college', 'keys', 'current_level', 'paidHintTaken', 'is_rigged', 'machine_used']



    def __str__(self):
        return self.username
    
class Question(models.Model):
    title = models.CharField(max_length=64, null=True)
    # https://nth22.s3.ap-south-1.amazonaws.com/transperent.png
    img1 = models.URLField(max_length = 1023, default="https://nth22.s3.ap-south-1.amazonaws.com/transperent.png")
    img2 = models.URLField(max_length = 1023, null=True, blank=True)
    img3 = models.URLField(max_length = 1023, null=True,blank=True)
    img4 = models.URLField(max_length = 1023, null=True,blank=True)
    level = models.IntegerField(unique=True, null=True)
    tooltip = models.CharField(max_length=1023, null=True, default=None)
    hints = models.TextField(default="<hints>")
    hintCost = models.IntegerField(null = True, blank=True)
    righints = models.TextField(default='[]',blank=True)
    
    # gif = models.URLField(max_length=1023, null=True, default=None)
    # vid = models.URLField(max_length=1023, null=True, default=None)

    # Confidential
    answer = models.CharField(max_length=1023, default="")
    rigword = models.CharField(max_length=1023, default="")
    keywords = models.TextField(default='[]',blank=True)
    paidHint = models.TextField(default="<Extra hint>")


    def __str__(self):
        return self.title + ": " + str(self.level)

    def save(self, *args, **kwargs):
        if not self.hintCost:
            self.hintCost = math.ceil(self.level * 1.5)
        super(Question, self).save(*args, **kwargs)


class Timer(models.Model):
    time = models.IntegerField(default=1666971000000)
    is_started = models.BooleanField(default=False)
    is_ended = models.BooleanField(null = True,default=False)
    promo_code_active = models.BooleanField(default=False)
    promocode = models.CharField(max_length=100, default="NTH22")
    add_keys_interval_min = models.IntegerField(default=120)

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    feedback = models.TextField()

    def __str__(self):
        return self.name

class AnswerHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answers = models.JSONField(default=list, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + " answered " + self.question.title
    