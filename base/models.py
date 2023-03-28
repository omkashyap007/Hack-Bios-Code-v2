from django.db import models
from django.contrib.auth.models import User

class PiGroup(models.Model):
    group_name      = models.CharField(max_length = 100)
    users           = models.ManyToManyField(User , null = True , related_name = "user_group")

    def __str__(self): 
        return str(self.group_name)
    