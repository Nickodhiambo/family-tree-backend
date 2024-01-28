from rest_framework import serializers
from .models import Family_Member


class Family_Member_Serializer(serializers.ModelSerializer):
    """Serializers and deserializes family member objects"""
    class Meta:
        model = Family_Member
        fields = ['id', 'name', 'gender', 'parent', 'children']


class Ancestors_Serializer(serializers.Serializer):
    """Serializes family chain"""
    chain = serializers.SerializerMethodField()

    def get_chain(self, obj):
        # This method should return the list of ancestors for the Family_Member instance
        return obj.chain() if hasattr(obj, 'chain') and callable(obj.chain) else []
