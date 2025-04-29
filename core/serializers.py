from rest_framework import serializers
from .models import SiteUser

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = SiteUser
        fields = ['first_name', 'last_name', 'username', 'password', 'role']

    def create(self, validated_data):
        user = SiteUser.objects.create_user(
            first_name=validated_data['first_name'],
            last_name =validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user
    

class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteUser
        fields = ['username', 'email', 'role']