from django.db import models

# Create your models here.

class Family_Member(models.Model):
    """An Individual family member"""
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [
            (MALE, 'Male'),
            (FEMALE, 'Female')
            ]

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    children = models.ManyToManyField('self', null=True, blank=True, related_name='parents', symmetrical=True)

    def get_chain(self):
        """Create a parent chain"""
        chain = []
        current_member = self
        chain.append(current_member)

        while current_member.parent:
            chain.append(current_member.parent)
            current_member = current_member.parent
        return chain

    def get_children_chain(self):
        """Gets the children chain of the current family member"""
        return Family_Member.objects.filter(parent=self)
