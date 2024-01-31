from django.db import models

# Create your models here.

class Family_Member(models.Model):
    """An Individual family member"""
    name = models.CharField(max_length=100, null=True)
    child = models.ForeignKey(
            'self',
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            related_name = 'parents'
        )

    
    def __str__(self):
        return (f"{self.parent}")

    def get_children_chain(self):
        """Gets the children tree of the current member"""
        family_tree = []
        child = self.child

        while child:
            family_tree.insert(0, child) # Append instead of insert
            child = child.child
        return reversed(family_tree)


    """def get_parents_chain(self):
        Gets the parents tree of the current member
        family_tree = [self]
        parent = self.parents.first()  # Assuming a member can have multiple parents

        while parent:
            family_tree.insert(0, parent)
            parent = parent.parents.first()

        return reversed(family_tree)"""
