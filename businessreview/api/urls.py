from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'reviews', views.ReviewViewSet, basename='review')
router.register(r'reported-reviews', views.ReportedReviewViewSet, basename='reported-review')
router.register(r'review-replies', views.ReviewReplyViewSet, basename='review-reply')

urlpatterns = [
    path('api/', include(router.urls)),
    path(
        'api/businesses/<slug:business_slug>/reviews/',
        views.ReviewViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='business-reviews'
    ),
]