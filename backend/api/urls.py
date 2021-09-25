from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

api_router = DefaultRouter()

api_router.register(r'tags', TagViewSet)
api_router.register(
    r'tags/(?P<tag_id>\d+)/',
    TagViewSet,
    basename='tags',
)
api_router.register(r'ingredients', IngredientViewSet)
api_router.register(
    r'ingredients/(?P<ingredient_id>\d+)/',
    IngredientViewSet,
    basename='ingredients',
)
api_router.register(
    r'recipes',
    RecipeViewSet,
    basename='recipes',
)


urlpatterns = [
    path('', include(api_router.urls)),
]
