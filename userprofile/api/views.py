from rest_framework import viewsets,permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response 
from django.contrib.auth import get_user_model
from .serializers import UserSerializer,UserRegistrationSerializer
from .permissions import IsOwnerOrAdmin

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer
    def get_permissions(self):
        if self.action == 'create':
            return[permissions.AllowAny()]
        elif self.action in ['update','partial_update','destroy']:
            return [IsOwnerOrAdmin()]
        return [permissions.IsAdminUser()]
    

class UserprofileView(APIView): 
    permission_classes = [IsAuthenticated]

    def get(self,request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    def put(self,request):
        serializer = UserSerializer(request.user, data=request.data,partail=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return  Response(serializer.error,status=400)
            