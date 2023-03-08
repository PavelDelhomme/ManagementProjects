from django.db import models
from users.models import UserProfile


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    members = models.ManyToManyField(UserProfile)

    def __str__(self): return self.name

class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text