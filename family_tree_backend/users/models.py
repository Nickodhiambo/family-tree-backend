from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
admin_group, _ = Group.objects.get_or_create(name='admin')
