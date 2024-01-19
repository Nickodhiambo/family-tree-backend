from rest_framework import serializers
from .models import Family_Member

class FamilyMemberSerializer(serializers.ModelSerializer):
    """Serializes and deserializers family member data"""
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Family_Member
        fields = '__all__'

    def get_parent(self, obj):
        family_tree = obj.get_family_tree()
        
	# Manually serialize each member in the family tree
        serialized_family_tree = []
        for member in family_tree:
            serialized_member = {
                'id': member.id,
                'user_name': member.user_name,
                'certificate_image': member.certificate_image.url if member.certificate_image else None,
                #'parent': []  # Set an empty list for the parent to avoid recursion
            }
            serialized_family_tree.append(serialized_member)

        return serialized_family_tree

"""class ParentListSerializer(serializers.ModelSerializer):
    Serializes the parent list API
    parent = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Family_Member
        fields = ['id', 'user_name', 'parent', 'children']
        depth = 1

    def get_parent(self, obj):
        Serializes parent object
        parent = obj.parent
        return ParentListSerializer(parent).data if parent else None

    def get_children(self, obj):
        Serializes children objects
        children = ParentListSerializer(obj.children.all(), many=True).data
        return children if children else []"""

class ImmediateChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Family_Member
        fields = ['id', 'user_name']

class ParentListSerializer(serializers.ModelSerializer):
    """Serializes the parent list API"""
    parent = ImmediateChildrenSerializer(read_only=True)
    children = ImmediateChildrenSerializer(many=True, read_only=True)

    class Meta:
        model = Family_Member
        fields = ['id', 'user_name', 'parent', 'children']
class NewSerializer(serializers.ModelSerializer):
    parents = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Family_Member
        fields = ['id', 'user_name', 'certificate_image', 'parents']

    def to_internal_value(self, data):
        # Convert the comma-separated string of parents into a list
        if 'parents' in data and isinstance(data['parents'], str):
            data['parents'] = [parent.strip() for parent in data['parents'].split(',')]

            return super().to_internal_value(data)

    def get_parents(self, obj):
        # Retrieve and serialize information about the entire lineage of parents
        parents = obj.get_family_tree()
        return NewSerializer(parents, many=True).data
