# Generated by Django 3.2.21 on 2024-01-28 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trees', '0010_alter_family_member_children'),
    ]

    operations = [
        migrations.AlterField(
            model_name='family_member',
            name='children',
            field=models.ManyToManyField(blank=True, null=True, related_name='_trees_family_member_children_+', to='trees.Family_Member'),
        ),
    ]
