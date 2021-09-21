from rest_framework import permissions, viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

from .permissions import IsAdminOrReadOnly
from .models import ShoppingCart, Tag, Ingredient, Recipe, Favorite
from .serializers import (
    ShoppingCartSerializer,
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
    FavoriteSerializer,
)
from rest_framework.response import Response
import pdb


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly, )


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly, )


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
        )
        return serializer

    @action(methods=['get', 'delete'], detail=True, permission_classes=(permissions.IsAuthenticated, ))
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'GET':

            if (Favorite.objects.filter(user=user, recipe=recipe)
                    .exists()):
                return Response({
                    'errors': ('Рецепт уже добавлен в избранное')
                }, status=status.HTTP_400_BAD_REQUEST)

            favorite = Favorite.objects.create(user=user, recipe=recipe)
            favorite.save()
            serializer = FavoriteSerializer(
                favorite, context={'request': request}
            )
            # pdb.set_trace ()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        favorite = Favorite.objects.filter(
            user=user, recipe=recipe
        )

        if favorite.exists():
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({
            'errors': 'Рецепт не находится в избранном'
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get', 'delete'], detail=True, permission_classes=(permissions.IsAuthenticated, ))
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'GET':

            if (ShoppingCart.objects.filter(user=user, recipe=recipe)
                    .exists()):
                return Response({
                    'errors': ('Рецепт уже добавлен в список покупок')
                }, status=status.HTTP_400_BAD_REQUEST)

            shopping_cart = ShoppingCart.objects.create(user=user, recipe=recipe)
            shopping_cart.save()
            serializer = ShoppingCartSerializer(
                shopping_cart, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        shopping_cart = ShoppingCart.objects.filter(
            user=user, recipe=recipe
        )

        if shopping_cart.exists():
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({
            'errors': 'Рецепт не находится в списке покупок'
        }, status=status.HTTP_400_BAD_REQUEST)
