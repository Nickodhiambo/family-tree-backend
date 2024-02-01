from rest_framework import serializers
from .models import Family_Member


class FamilyMemberSerializer(serializers.ModelSerializer):
    """Serializes and deserializers family member data"""
    children = serializers.SerializerMethodField()

    class Meta:
        model = Family_Member
        fields = ['id', 'name', 'children']

    def get_children(self, obj):
        family_tree = obj.get_children_chain()
        
	# Manually serialize each member in the family tree
        serialized_family_tree = []
        for member in family_tree:
            serialized_member = {
                'id': member.id,
                'name': member.name,
            }
            serialized_family_tree.append(serialized_member)
        return serialized_family_tree


class NewSerializer(serializers.ModelSerializer):
    children = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Family_Member
        fields = ['id', 'name', 'children']

    def to_internal_value(self, data):
        # Convert the comma-separated string of children into a list
        if 'children' in data and isinstance(data['children'], str):
            data['children'] = [child.strip() for child in data['children'].split(',')]
            return super().to_internal_value(data)
    def get_children(self, obj):
        # Retrieve and serialize information about the entire lineage of children
        children = obj.get_children_chain()
        return NewSerializer(children, many=True).data


class ImmediateParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Family_Member
        fields = ['id', 'name']


class ParentListSerializer(serializers.ModelSerializer):
    #parents = ImmediateParentSerializer(many=True, read_only=True)
    parents = serializers.SerializerMethodField()

    class Meta:
        model = Family_Member
        fields = ['parents']

    def get_parents(self, obj):
        family_tree = obj.get_parents_chain(obj)
        serialized_family_tree = []
        for member in family_tree:
            serialized_member = {
                    'id': member.id,
                    'name': member.name
                    }
            serialized_family_tree.append(serialized_member)
        return serialized_family_tree
