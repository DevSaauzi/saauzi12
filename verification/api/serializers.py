from rest_framework import serializers
from verification.models import Verification

class VerificationSerializer(serializers.ModelSerializer):
    business_name = serializers.CharField(source="business.name",read_only=True)
    business_email = serializers.CharField(source="business.email",read_only = True)
    class Meta:
        model = Verification
        fields = ['id','business_name','business_email', 'pan_number', 'citizenship_number', 'owner_name','meta_title','meta_description',]
    

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['verification'] ={
            'documents':{
                'pan':instance.is_pan_verified,
                'citizenship':instance.is_citizenship_verified,
                'verified':instance.is_pan_verified and instance.is_citizenship_verified
            },
            'seo':{
                'meta_tags_valid':instance.has_valid_metatags,
                'title':instance.meta_title or instance.business.met_title,
                'description':instance.meta_description or instance.business.meta_description 
            },
            'email':{
                'domain_verified':instance.is_email_domain_verified,
                'business_email':instance.instance.business.email

            },
            'status':{
                'fully_verified':instance.is_fully_verified,
                'pending_steps':instance.pendings_steps,
                'summary':instance.verification_summary
            }

        }  
        return data  