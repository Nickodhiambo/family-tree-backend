from rest_framework import serializers
from .models import Family_Member


class ChildrenSerializer(serializers.ModelSerializer):
    """Serializes id and name fields of direct children"""

    class Meta:
        model = Family_Member
        fields = ['id', 'name']


class Family_Member_Serializer(serializers.ModelSerializer):
    """Serializers and deserializes family member objects"""

    children = ChildrenSerializer(many=True, read_only=True)

    class Meta:
        model = Family_Member
        fields = ['id', 'name', 'gender', 'parent', 'children']


class Ancestors_Serializer(serializers.Serializer):
    """Serializes family chain"""
    chain = Family_Member_Serializer(many=True)

    def to_representation(self, instance):
        """Returns a list of ancestors to a member"""
        return {'chain': Family_Member_Serializer(instance.get_chain(), many=True).data}
