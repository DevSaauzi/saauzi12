from rest_framework import serializers
from businessreview.models import Review,ReportedReview,ReviewReply
from listings.models import BusinessListing
from userprofile.models import User
from userprofile.api.serializers import UserSerializer
from listings.api.serializers import BusinessListingSerializer




class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    business = BusinessListingSerializer(read_only=True)
    is_reported = serializers.BooleanField(read_only=True)
    weighted_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Review
        fields = ['id','business','author','rating','comment','is_verified','media','is_reported',          
            'weighted_rating', 'created_at', 'updated_at',]
        read_only_fields = ['id','author','rating','is_verified','is_reported','weighted_rating','created_at','updated_at']






class ReportedReviewSerializer(serializers.ModelSerializer):
    reviewed = ReviewSerializer(read_only=True)
    reported_by = UserSerializer(read_only=True)
    resolved_by = UserSerializer(read_only = True)
   

    class Meta:
        model = ReportedReview
        fields = ['id','reviewed','reported_by','reason','status','resolved_by']
        read_only_fields = ['id','reported_by','resolved_by']


    def validate(self, data):
        request = self.context.get('request')
        review = self.context['view'].get_object()
        if request and request.user != review.business.owner:
            raise serializers.ValidationError(
                "Only the business owner can reply to this review."
            )
        return data

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        validated_data['review'] = self.context['view'].get_object()
        return super().create(validated_data)





class ReviewReplySerializer(serializers.ModelSerializer) :
    owner = UserSerializer(read_only=True)
    review = ReviewSerializer(read_only = True)

    class Meta:
        model = ReviewReply
        fields = ['id','review','owner','message','created_at','updated_at', ]
        read_only_fields = ['id', 'owner', 'review', 'created_at', 'updated_at']


    def  validate(self,data):
        request = self.context.get('request')
        review = self.context.get['view'].get_object()
        if request and request.user != review.business.owner:
            raise serializers.ValidationErrors("Only the business owner can reply these review")

    def create(self,validated_data):
        validated_data['data'] = self.context['request'].user
        validated_data['review'] = self.context['view'].get_object()
        return super().create(validated_data)