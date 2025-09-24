from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'subcategories', views.SubCategoryViewSet)
router.register(r'businesses', views.BusinessListingViewSet)
router.register(r'locations', views.BusinessLocationViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
]