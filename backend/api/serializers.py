from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import (Favorite, Ingredient, Purchase, Recipe, RecipeIngredient,
                     Subscription, Tag)


class CustomModelSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return self.Meta.model.objects.create(**validated_data)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('title', 'dimension',)


class SubscriptionSerializer(CustomModelSerializer):
    class Meta:
        model = Subscription
        fields = ('user', 'author',)

    def validate_author(self, value):
        user = self.context['request'].user
        if user.id == value:
            raise ValidationError('Нельзя подписаться на самого себя')
        return value


class FavoriteSerializer(CustomModelSerializer):
    class Meta:
        model = Favorite
        fields = ('recipe', )


class PurchaseSerializer(CustomModelSerializer):
    class Meta:
        model = Purchase
        fields = ('recipe', )


class TagSerializer(CustomModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'slug', 'style',)


class RecipeSerializer(CustomModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeIngredientSerializer(CustomModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ('recipe', 'ingredient', 'amount',)
