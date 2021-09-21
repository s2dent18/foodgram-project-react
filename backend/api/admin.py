from django.contrib import admin

from .models import Favorite, ShoppingCart, Tag, Ingredient, Recipe, RecipeIngredient


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    empty_value_display = '-empty-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)
    empty_value_display = '-empty-'


class IngredientInLine(admin.TabularInline):
    model = RecipeIngredient


class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        IngredientInLine,
    ]
    list_display = (
        'name',
        'author',
    )
    list_filter = ("name", "author", "tags")
    empty_value_display = "-empty-"


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "recipe")
    empty_value_display = "-empty-"


class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "recipe")
    empty_value_display = "-empty-"


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, CartAdmin)
