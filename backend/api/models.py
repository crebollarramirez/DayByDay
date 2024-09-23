from django.db import models

# Create your models here.
class Task(models.Model):
    content = models.TextField()
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    done = False

    def __str__(self):
        return self.content
    
# class DailyTask(models.Model):
