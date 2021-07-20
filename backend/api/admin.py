from django.contrib import admin
from django.contrib.admin.decorators import register
from django.db.models.aggregates import Count

from .models import (Favorite, Ingredient, Purchase, Recipe, RecipeIngredient,
                     Subscription, Tag)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    autocomplete_fields = ('user', 'recipe')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    autocomplete_fields = ('user', 'author')


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    autocomplete_fields = ('user', 'recipe')


@register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension',)
    empty_value_display = '-пусто-'
    search_fields = (
        'title',
    )
    list_filter = (
        'title',
    )


@register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    fields = (
        'ingredient',
        'recipe',
        'amount',
    )
    search_fields = (
        'ingredient',
        'recipe',
    )


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1


@register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'slug',
        'style',
    )
    search_fields = (
        'name',
    )


@register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'recipe_follower_count',)
    readonly_fields = ('recipe_follower_count',)
    fields = (
        'author',
        'title',
        'image',
        'text',
        'tags',
        'time',
        'slug',
        'recipe_follower_count',
    )
    search_fields = (
        'title',
        'author__username',
    )
    list_filter = (
        'title',
        'author__username',
        'tags',
    )
    autocomplete_fields = (
        'ingredients',
    )
    inlines = (
        RecipeIngredientInline,
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(recipe_follower_count=Count('following'))
        return qs

    def recipe_follower_count(self, obj):
        return obj.recipe_follower_count
    recipe_follower_count.short_description = 'Добавлений в избранное'
