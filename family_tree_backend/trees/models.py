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
    children = models.ManyToManyField('self', null=True, blank=True, related_name='parent')

    def get_chain(self):
        """Create a parent chain"""
        chain = []
        current_member = self
        chain.append(current_member)

        while current_member.parent:
            chain.append(current_member.parent)
            current_member = current_member.parent
        return list(reversed(chain))


    def get_children_chain(self):
        """Gets all the children to a member"""
        children_chain = []
        for child in Family_Member.objects.filter(parent=self):
            children_chain.append({
                "id": child.id,
                "name": child.name,
            })

        return children_chain 
