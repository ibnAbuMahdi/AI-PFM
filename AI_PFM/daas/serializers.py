from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DAASUser
        fields = ['id', 'email', 'name', 'username', 'activated', 'code', 'is_agent']
        extra_kwargs = {
            'password': {"write_only": True}
        }
    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance
    
class ProspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prospect
        fields = '__all__'
        
