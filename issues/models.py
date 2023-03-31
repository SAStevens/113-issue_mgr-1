from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class Status(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    def __str__(self):
        return self.name
    

class Priority(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    def __str__(self):
        return self.name


class Issue(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    priority = models.ForeignKey(
        Priority,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    assignee = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="assignee",
        blank=True,
        null=True
    )
    

    def __str__(self):
        return self.summary
    
    def get_absolute_url(self):
        return reverse("detail", args=[self.id])
