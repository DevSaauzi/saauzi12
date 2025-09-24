
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,UserprofileView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('userprofile/api/', include(router.urls)),       
    path('userprofile/api/me/',UserprofileView.as_view(), name='user-profile'), 
]