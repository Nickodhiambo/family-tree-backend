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
                'parent': []  # Set an empty list for the parent to avoid recursion
            }
            serialized_family_tree.append(serialized_member)

        return serialized_family_tree
