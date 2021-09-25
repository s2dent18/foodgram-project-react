from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet

user_router = DefaultRouter()

user_router.register(
    r'users',
    CustomUserViewSet,
    basename='subscribe',
)

urlpatterns = [
    path('', include(user_router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
