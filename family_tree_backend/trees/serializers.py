from rest_framework import serializers
from .models import Family_Member


class Base_Serializer(serializers.ModelSerializer):
    """Serializes all fields"""

    class Meta:
        model = Family_Member
        fields = ['id', 'name', 'parent', 'children']


class Family_Member_Serializer(serializers.ModelSerializer):
    """Serializers and deserializes family member objects"""

    children = serializers.SerializerMethodField()

    class Meta:
        model = Family_Member
        fields = ['id', 'name', 'parent', 'children']

    def get_children(self, instance):
        children_data = Family_Member.objects.filter(parent=instance).values('id', 'name')
        return children_data


class Ancestors_Meta(serializers.ModelSerializer):
    class Meta:
        model = Family_Member
        fields = ['id', 'name']


class Ancestors_Serializer(serializers.ModelSerializer):
    """Serializes family chain"""

    def to_representation(self, instance):
        """Returns a list of ancestors to a member"""
        return {'parents_chain': Ancestors_Meta(instance.get_chain(), many=True).data}
