from rest_framework import serializers
from notifications.models import Notifications, NotificationsPreference
from userprofile.models import User
from listings.models import BusinessListing
from businessreview.models import Review
from userprofile.api.serializers import UserSerializer
from listings.api.serializers import BusinessListingSerializer
from businessreview.api.serializers import ReviewSerializer



class NotificationSerializer(serializers.ModelSerializer):
    recipient = UserSerializer(read_only=True)
    related_business = BusinessListingSerializer(read_only=True)
    related_review = ReviewSerializer(read_only=True)

    class Meta:
        model = Notifications
        fields = [
            'id',
            'recipient',
            'event_type',
            'related_business',
            'related_review',
            'related_promotion',
            'subject',
            'message',
            'sent_at',
            'read_status',
            'delivery_channel',
            'priority',
        ]
        read_only_fields = ['sent_at']


class NotificationCreateSerializer(serializers.ModelSerializer):
    recipient = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    related_business = serializers.PrimaryKeyRelatedField(queryset=BusinessListing.objects.all())
    related_review = serializers.PrimaryKeyRelatedField(
        queryset=Review.objects.all(), required=False, allow_null=True
    )
    related_promotion = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Notifications
        fields = [
            'recipient',
            'event_type',
            'related_business',
            'related_review',
            'related_promotion',
            'subject',
            'message',
            'delivery_channel',
            'priority',
        ]

    def validate_event_type(self, value):
        valid = [c[0] for c in Notifications.EVENT_TYPES]
        if value not in valid:
            raise serializers.ValidationError(f"Invalid event type: {value}")
        return value

    def validate_delivery_channel(self, value):
        valid = [c[0] for c in Notifications.DELIVERY_CHANNELS]
        if value not in valid:
            raise serializers.ValidationError(f"Invalid delivery channel: {value}")
        return value

    def validate_priority(self, value):
        valid = [c[0] for c in Notifications.PRIORITY_CHOICES]
        if value not in valid:
            raise serializers.ValidationError(f"Invalid priority: {value}")
        return value


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationsPreference
        fields = ['user', 'events_enabled', 'delivery_channels', 'updated_at']
        read_only_fields = ['user', 'updated_at']  # user is set automatically

    def validate_events_enabled(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Must be a list.")
        valid = [c[0] for c in Notifications.EVENT_TYPES]
        invalid = set(value) - set(valid)
        if invalid:
            raise serializers.ValidationError(f"Invalid event types: {', '.join(invalid)}")
        return value

    def validate_delivery_channels(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Must be a list.")
        valid = [c[0] for c in Notifications.DELIVERY_CHANNELS]
        invalid = set(value) - set(valid)
        if invalid:
            raise serializers.ValidationError(f"Invalid delivery channels: {', '.join(invalid)}")
        return value

    