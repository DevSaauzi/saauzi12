from rest_framework import viewsets, status
from .serializers import VerificationSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from verification.models import Verification
from verification.services import run_initial_verification, send_email_otp, verify_email_otp


class VerificationViewSet(viewsets.ModelViewSet):
    serializer_class = VerificationSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch']
    
    def get_queryset(self):
        business = self.request.user.businesses.first()
        if not business:
            return Verification.objects.none()
        return Verification.objects.filter(business=business)
    
    def perform_create(self, serializer):
        business = self.request.user.businesses.first()
        if not business:
            raise serializer.ValidationError("You must own a business")
        serializer.save(business=business)
    
    def retrieve(self, request, *args, **kwargs):
        business = request.user.businesses.first()
        if not business:
            return Response({"error": "You don't own a business listing."}, status=status.HTTP_404_NOT_FOUND)
        verification, _ = Verification.objects.get_or_create(business=business)
        serializer = self.get_serializer(verification)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        business = request.user.businesses.first()
        if not business:
            return Response(
                {"error": "You don't own a business listing."},
                status=status.HTTP_404_NOT_FOUND
            )
        verification, _ = Verification.objects.get_or_create(business=business)
        allowed_fields = [
            'pan_card', 'citizenship', 'pan_number',
            'citizenship_number', 'owner_name',
            'meta_title', 'meta_description'
        ]
        for field in allowed_fields:
            if field in request.data:
                setattr(verification, field, request.data[field])
        verification.save()
        run_initial_verification(verification)
        serializer = self.get_serializer(verification)
        return Response(serializer.data)


    @action(detail=False, methods=['post'], url_path='send-otp')
    def send_otp(self, request):
        business = request.user.businesses.first()
        if not business:
            return Response(
                {"error": "You don't own a business listing."},
                status=status.HTTP_404_NOT_FOUND
            )
        verification, _ = Verification.objects.get_or_create(business=business)
        try:
            send_email_otp(verification)
            return Response({"message": "OTP sent to your business email."})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'], url_path='verify-otp')
    def verify_otp(self, request):
        business = request.user.businesses.first()
        if not business:
            return Response(
                {"error": "You don't own a business listing."},
                status=status.HTTP_404_NOT_FOUND
            )
        verification = get_object_or_404(Verification, business=business)
        otp = request.data.get('otp')
        if not otp:
            return Response({"error": "OTP is required."}, status=status.HTTP_400_BAD_REQUEST)

        if verify_email_otp(verification, otp):
            serializer = self.get_serializer(verification)
            return Response({
                "message": "Email verified successfully!",
                "verification": serializer.data
            })
        else:
            return Response({
                "error": "Invalid or expired OTP."
            }, status=status.HTTP_400_BAD_REQUEST)