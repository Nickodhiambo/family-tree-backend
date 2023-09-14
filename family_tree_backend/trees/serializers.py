from rest_framework import serializers
from .models import Family_Member

class FamilyMemberSerializer(serializers.ModelSerializer):
    """Serializes and deserializers family member data"""
    class Meta:
        model = Family_Member
        fields = '__all__'
