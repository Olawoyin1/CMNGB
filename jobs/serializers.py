from rest_framework import serializers
from .models import Job, Proposal, Category



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']





class JobSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField()
    category = serializers.SlugRelatedField( slug_field='name', queryset=Category.objects.all())
    # category = serializers.StringRelatedField(read_only=True)


    
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['client']
        
        
        

class ProposalSerializer(serializers.ModelSerializer):
    freelancer = serializers.StringRelatedField(read_only=True)
    job_detail = serializers.StringRelatedField(source='job', read_only=True)
    client = serializers.StringRelatedField(read_only=True)  


    
    class Meta:
        model = Proposal
        fields = '__all__'
        read_only_fields = ['freelancer', 'client']


# class MessageSerializer(serializers.ModelSerializer):
#     sender = serializers.StringRelatedField(source="user", read_only=True)
#     recipient = serializers.StringRelatedField(source="user", read_only=True)

#     class Meta: 
#         model = Message
#         fields = '__all__'
#         read_ony_fields = ['sender', 'recipient']