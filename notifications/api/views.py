from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from notifications.models import Notifications, NotificationsPreference
from .serializers import NotificationSerializer, NotificationPreferenceSerializer
from .permissions import NotificationAccessPermission


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = NotificationAccessPermission
    filter_backends = DjangoFilterBackend,OrderingFilter
    filterset_fields = ['read_status', 'event_type']
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']

    def get_queryset(self):
        user = self.request.user
        base_qs = Notifications.objects.select_related(
            'recipient', 'related_business', 'related_review'
        )
        if user.role == 'admin':
            return base_qs
        return base_qs.filter(recipient=user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.read_status and instance.recipient == request.user:
            instance.read_status= True
            instance.save(update_fields =['read_status'])
            return super.retrieve(request,*args,**kwargs)
   
    @action(detail=True, methods=['post'], url_path='read')
    def mark_read(self, request,pk=None):
        notification = self.get_object()
        if notification.recipient == request.user or request.user.role == "admin":
            notification.read_status = True
            notification.save(update_fields=['read_status'])
            return Response({'status': 'read'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Not allowed.'}, status=status.HTTP_403_FORBIDDEN)



class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [NotificationAccessPermission]
    
    def get_queryset(self):
        return NotificationsPreference.objects.filter(user = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def create(self,request,*args,**kwargs):
        existing = self.get_queryset().first()
        if existing:
            serializer = self.get_serializer(existing,data = request.data,partial=False)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().create(request, *args, **kwargs)