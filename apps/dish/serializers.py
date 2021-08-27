from typing import (
    List,
    Dict,
)

from django.db import transaction
from rest_framework import serializers

from . import models


# Ingredient
class IngredientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingredient
        fields = [
            "id",
            "name",
        ]
        read_only_fields = fields


class IngredientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingredient
        fields = [
            "id",
            "name",
        ]


class IngredientRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingredient
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class IngredientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingredient
        fields = [
            "id",
            "name",
        ]


# Dish
class DishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dish
        fields = [
            "id",
            "name",
        ]
        read_only_fields = fields


class DishCreateSerializer(serializers.ModelSerializer):
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True, queryset=models.Ingredient.objects.all()
    )

    class Meta:
        model = models.Dish
        fields = [
            "id",
            "name",
            "ingredients",
        ]


class DishIngredientRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingredient
        fields = [
            "id",
            "name",
        ]


class DishRetrieveSerializer(serializers.ModelSerializer):
    ingredients = DishIngredientRetrieveSerializer(many=True)

    class Meta:
        model = models.Dish
        fields = [
            "id",
            "name",
            "ingredients",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class DishUpdateSerializer(serializers.ModelSerializer):
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True, queryset=models.Ingredient.objects.all()
    )

    class Meta:
        model = models.Dish
        fields = [
            "id",
            "name",
            "ingredients",
        ]
        read_only_fields = []


# Order
class OrderDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dish
        fields = [
            "id",
            "name",
        ]


class OrderListSerializer(serializers.ModelSerializer):
    dish = OrderDishSerializer()

    class Meta:
        model = models.Order
        fields = [
            "id",
            "dish",
            "created_at",
        ]
        read_only_fields = fields


class OrderIngredientCreateSerializer(serializers.Serializer):
    ingredient_id = serializers.IntegerField()
    ingredients_amount = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.ModelSerializer):
    order_ingredients = OrderIngredientCreateSerializer(many=True)

    class Meta:
        model = models.Order
        fields = [
            "id",
            "dish",
            "order_ingredients",
        ]

    def create(self, validated_data):
        dish_id: int = validated_data["dish"].id
        ingredients: List[Dict[str, int]] = validated_data[
            "order_ingredients"
        ]

        with transaction.atomic():
            order: models.Order = models.Order.objects.create(dish_id=dish_id)

            order_ingredients: List[models.OrderIngredients] = [
                models.OrderIngredients(order=order, **ingredient)
                for ingredient in ingredients
            ]

            models.OrderIngredients.objects.bulk_create(order_ingredients)

        return order


class OrderIngredientRetrieveSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="ingredient_id")
    name = serializers.CharField(source="ingredient.name")
    amount = serializers.IntegerField(source="ingredients_amount")

    class Meta:
        model = models.OrderIngredients
        fields = [
            "id",
            "amount",
            "name",
        ]
        read_only_fields = fields


class OrderRetrieveSerializer(serializers.ModelSerializer):
    dish = OrderDishSerializer()
    ingredients = OrderIngredientRetrieveSerializer(
        source='order_ingredients', many=True
    )

    class Meta:
        model = models.Order
        fields = [
            "id",
            "dish",
            "ingredients",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
