from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.paginations import LimitPagination
from .models import Follow
from .serializers import FollowSerializer, UserSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    serializer_class = UserSerializer
    pagination_class = LimitPagination

    @action(
        methods=['get', 'delete'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated, )
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)

        if request.method == 'GET':

            if (Follow.objects.filter(user=user, author=author)
                    .exists() or user == author):
                return Response({
                    'errors': ('Вы уже подписаны на этого пользователя '
                               'или подписываетесь на самого себя')
                }, status=status.HTTP_400_BAD_REQUEST)

            subscribe = Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(
                subscribe,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        subscribe = Follow.objects.filter(
            user=user, author=author
        )

        if subscribe.exists():
            subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({
            'errors': 'Вы не подписаны на этого пользователя'
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=(permissions.IsAuthenticated, ))
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
