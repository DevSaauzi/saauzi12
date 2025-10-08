from django.urls import path,include
from rest_framework.routers import DefaultRouter
from verification.api.views  import VerificationViewSet

router = DefaultRouter()
router.register(r'verification',VerificationViewSet,basename='verification')

urlpatterns = [
    path('api/',include(router.urls)),
]