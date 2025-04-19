from django.db import models
from django.contrib.auth.models import User

class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    date = models.DateField()
    estimated_time = models.PositiveIntegerField()  # Time in minutes

    def __str__(self):
        return f"{self.topic} - {self.date}"

class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    study_time = models.PositiveIntegerField()  # Time spent in minutes
    date = models.DateField()

    def __str__(self):
        return f"{self.topic} on {self.date} ({self.study_time} minutes)"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class Friendship(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.friend.username}"
    
class ActivityFeed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"
