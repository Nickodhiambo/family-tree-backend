from django.db import models

# Create your models here.

class Family_Member(models.Model):
    """An Individual family member"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    parent = models.ForeignKey(
            'self',
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            related_name = 'children'
        )
    
    def __str__(self):
        return (f"{self.first_name} {self.last_name}")
