from django.db import models

class Thread(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

class Comment(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    content = models.TextField()


# Create your models here.
