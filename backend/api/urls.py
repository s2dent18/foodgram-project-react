from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TagViewSet,
    IngredientViewSet,
    RecipeViewSet,
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
    r"recipes",
    RecipeViewSet,
    basename="recipes",
)


urlpatterns = [
    path('', include(router.urls)),
]
