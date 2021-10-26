from django.db import models

class water(models.Model):
    name = models.CharField(max_length=50, null=False)
    water = models.CharField(max_length=50, null=False)
    last_update = models.DateTimeField(auto_now=True)  # auto_now default: UTC+0
    
    def __str__(self):
        return self.name