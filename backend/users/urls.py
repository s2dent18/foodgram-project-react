from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, FollowViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register(
    r'users/(?P<user_id>\d+)/subscribe',
    FollowViewSet,
    basename='subscribe',
)
router.register(
    r'users/subscriptions',
    FollowViewSet,
    basename='subscriptions'
)

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
