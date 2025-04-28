from rest_framework import serializers
from .models import User, Profile, Skill





class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']
        
        
class UserRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'is_staff',
            'date_joined',
            'role'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'date_joined': {'read_only': True},
            'is_staff': {'required': False},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)  # pop password if it's being updated
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)  # hash and set the password correctly

        instance.save()
        return instance
    
    
class ProfileSerializer(serializers.ModelSerializer):
    user_detail = serializers.StringRelatedField(source='user', read_only=True) 

    class Meta:
        model = Profile
        fields = '__all__'
        
        
        
    def update(self, instance, validated_data):
        skills_data = validated_data.pop('skills', [])
        instance = super().update(instance, validated_data)

        if skills_data:
            skill_objs = []
            for skill in skills_data:
                obj, _ = Skill.objects.get_or_create(name=skill['name'])
                skill_objs.append(obj)
            instance.skills.set(skill_objs)

        return instance
