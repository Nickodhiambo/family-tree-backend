from rest_framework import serializers
from .models import Family_Member


class FamilyMemberSerializer(serializers.ModelSerializer):
    """Serializes and deserializers family member data"""
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Family_Member
        fields = ['id', 'name', 'parent']

    def get_parent(self, obj):
        family_tree = obj.get_family_tree()
        
	# Manually serialize each member in the family tree
        serialized_family_tree = []
        for member in family_tree:
            serialized_member = {
                'id': member.id,
                'name': member.name,
            }
            serialized_family_tree.append(serialized_member)
        return serialized_family_tree


class ImmediateChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Family_Member
        fields = ['id', 'name']
class ParentListSerializer(serializers.ModelSerializer):
    """Serializes the parent list API"""
    parent = ImmediateChildrenSerializer(read_only=True)
    children = ImmediateChildrenSerializer(many=True, read_only=True)
    class Meta:
        model = Family_Member
        fields = ['id', 'name', 'parent', 'children']
class NewSerializer(serializers.ModelSerializer):
    parents = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Family_Member
        fields = ['id', 'name', 'parents']

    def to_internal_value(self, data):
        # Convert the comma-separated string of parents into a list
        if 'parents' in data and isinstance(data['parents'], str):
            data['parents'] = [parent.strip() for parent in data['parents'].split(',')]
            return super().to_internal_value(data)
    def get_parents(self, obj):
        # Retrieve and serialize information about the entire lineage of parents
        parents = obj.get_family_tree()
        return NewSerializer(parents, many=True).data
