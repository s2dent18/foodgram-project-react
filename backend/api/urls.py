from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TagViewSet,
    IngredientViewSet,
    RecipeViewSet,
    FavoriteViewSet,
)

router = DefaultRouter()

router.register(r"tags", TagViewSet)
router.register(
    r"tags/(?P<tag_id>\d+)/",
    TagViewSet,
    basename="tags",
)
router.register(r"ingredients", IngredientViewSet)
router.register(
    r"ingredients/(?P<ingredient_id>\d+)/",
    IngredientViewSet,
    basename="ingredients",
)
router.register(
    r"recipes/(?P<recipe_id>\d+)/favorite",
    FavoriteViewSet,
    basename="favorite",
)
router.register(r"recipes", RecipeViewSet)
router.register(
    r"recipes/(?P<recipe_id>\d+)/",
    RecipeViewSet,
    basename="recipes",
)


urlpatterns = [
    path('', include(router.urls)),
]
