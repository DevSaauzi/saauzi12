from django.urls import path,include
from rest_framework.routers import DefaultRouter
from  .import views

router = DefaultRouter()
router.register(r'weekly-rankings',views.WeeklyRankingViewSet,basename='weekly-rankings')
router.register(r'monthly-rankings',views.MonthlyRankingViewSet,basename='monthly-rankings')

urlpatterns = [
    path('api/v1/analytics',include(router.urls)),
     path( 'api/v1/analytics/business-views/',views.BusinessViewViewSet.as_view({'post': 'create'}),
        name='business-view'),
    path('api/v1/analytics/contact-clicks/', views.ContactClickViewSet.as_view({'post': 'create'}),
        name='contact-click')
]