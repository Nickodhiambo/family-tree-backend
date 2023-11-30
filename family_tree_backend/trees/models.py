from django.db import models

# Create your models here.

class Family_Member(models.Model):
    """An Individual family member"""
    first_name = models.CharField(max_length=100)
    #last_name = models.CharField(max_length=100)
    parent = models.ForeignKey(
            'self',
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            related_name = 'children'
        )

    certificate_image = models.ImageField(upload_to='certificates/', blank=True, null=True)
    data_coordinates = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return (f"{self.first_name}")

    def get_family_tree(self):
        """Gets the parent tree of the current member"""
        family_tree = [self]
        parent = self.parent

        while parent:
            family_tree.insert(0, parent)
            parent = parent.parent
        return family_tree
