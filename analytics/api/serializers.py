from rest_framework import serializers
from analytics.models import BusinessView,WeeklyRanking,MonthlyRanking, ContactClick



class BusinessViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessView
        fields = ['business','ip_address','user_agent',]


    def validate(self,validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data) 



class ContactClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactClick
        fields = ['business','contact_type','ip_address']

    def validate_contact_type(self,value):
        allowed = dict(ContactClick.CONTACT_TYPE_CHOICES).keys()
        if value not in allowed:
         raise serializers.ValidationError(f"Invalid contact type. Choose from: {list(allowed)}") 
        return value
    

    def validate(self,validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)
    
class WeeklyRankingSerializer(serializers.ModelSerializer):
    business__name = serializers.SerializerMethodField()
    class Meta:
        model = WeeklyRanking
        fields = [
            'id', 'business', 'business__name', 'week_start', 'view_count',
            'click_count', 'review_count', 'average_rating', 'ranking_score', 'ranking'
        ]


class MonthlyRankingSerializer(serializers.ModelSerializer):
    business_name = serializers.CharField(source='business.name', read_only=True)
    
    class Meta:
        model = MonthlyRanking
        fields = [
            'id', 'business', 'business_name', 'year', 'month', 'view_count',
            'click_count', 'review_count', 'average_rating', 'ranking_score', 'ranking'
        ]        