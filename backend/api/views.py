from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)
from .paginations import LimitPagination
from .permissions import AuthorOrReadOnly, ReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, ShoppingCartSerializer,
                          TagSerializer)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (ReadOnly, )


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (ReadOnly, )
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = RecipeFilter
    permission_classes = (AuthorOrReadOnly, )
    pagination_class = LimitPagination

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
        )

    @action(
        methods=['get', 'delete'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated, )
    )
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
            serializer = FavoriteSerializer(
                favorite, context={'request': request}
            )
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

    @action(
        methods=['get', 'delete'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated, )
    )
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'GET':

            if (ShoppingCart.objects.filter(user=user, recipe=recipe)
                    .exists()):
                return Response({
                    'errors': ('Рецепт уже добавлен в список покупок')
                }, status=status.HTTP_400_BAD_REQUEST)

            shopping_cart = ShoppingCart.objects.create(
                user=user, recipe=recipe)
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

    @action(
        methods=['get'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated, )
    )
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = RecipeIngredient.objects.filter(
            recipe__put_by__user=user).values_list(
                'ingredient__name',
                'amount',
                'ingredient__measurement_unit')
        shopping_list = {}

        for ingredient in ingredients:
            name = ingredient[0]
            amount = ingredient[1]
            measurement_unit = ingredient[2]

            if name not in shopping_list:
                shopping_list[name] = {
                    'measurement_unit': measurement_unit,
                    'amount': amount
                }
            else:
                shopping_list[name]['amount'] += amount

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.pdf"')
        pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf', 'UTF-8'))
        pdfmetrics.registerFont(TTFont(
            'FreeSansBold', 'FreeSansBold.ttf', 'UTF-8'))
        page = canvas.Canvas(response)
        page.setFont('FreeSansBold', size=22)
        page.setFillColor(colors.red)
        page.drawString(200, 800, 'Список покупок:')
        page.setFillColor(colors.black)
        page.line(50, 780, 550, 780)
        page.setFont('FreeSans', size=16)
        height = 750

        for name, data in shopping_list.items():
            page.drawString(
                50,
                height,
                (f'- { name } : {data["amount"]} '
                 f'{data["measurement_unit"]}')
            )
            height -= 25
            if height == 50:
                page.showPage()
                height = 800

        page.line(50, height, 550, height)
        page.setFillColor(colors.red)
        page.setFont('FreeSans', size=12)
        page.drawString(450, height - 25, '(с) Foodgram')
        page.showPage()
        page.save()
        ShoppingCart.objects.filter(user=user).delete()
        return response
