from typing import (
    List,
    Dict,
)

from django.db import transaction
from rest_framework import (
    viewsets,
    mixins,
)
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter

from . import models
from . import serializers


class IngredientViewSet(viewsets.ModelViewSet):
    """ViewSet for the Ingredient class"""

    queryset = models.Ingredient.objects.all()
    serializer_action_classes = {
        "list": serializers.IngredientListSerializer,
        "create": serializers.IngredientCreateSerializer,
        "retrieve": serializers.IngredientRetrieveSerializer,
        "update": serializers.IngredientUpdateSerializer,
        "partial_update": serializers.IngredientUpdateSerializer,
    }
    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at"]

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]


class DishViewSet(viewsets.ModelViewSet):
    """ViewSet for the Dish class"""

    queryset = models.Dish.objects.all()
    serializer_action_classes = {
        "list": serializers.DishListSerializer,
        "create": serializers.DishCreateSerializer,
        "retrieve": serializers.DishRetrieveSerializer,
        "update": serializers.DishUpdateSerializer,
        "partial_update": serializers.DishUpdateSerializer,
    }
    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at"]

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet for the Order class"""

    queryset = models.Order.objects.all()
    serializer_action_classes = {
        "list": serializers.OrderListSerializer,
        "create": serializers.OrderCreateSerializer,
        "retrieve": serializers.OrderRetrieveSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]

    def perform_create(self, serializer: serializers.OrderCreateSerializer):
        dish_id: int = serializer.validated_data["dish"].id
        ingredients: List[Dict[str, int]] = serializer.validated_data[
            "order_ingredients"
        ]

        ingredient_ids: List[int] = [
            element["ingredient_id"] for element in ingredients
        ]

        self.all_elements_is_unique(ingredient_ids=ingredient_ids)

        self.check_ingredients_exist(
            ingredient_ids=ingredient_ids, dish_id=dish_id
        )

        serializer.save()

    def all_elements_is_unique(self, ingredient_ids: List[int]):
        duplicate_error: str = (
            "You have a duplicate value: ingredient_id - {value}"
        )

        seen: set = set()

        for ingredient_id in ingredient_ids:
            if ingredient_id in seen:
                raise ValidationError(
                    duplicate_error.format(value=ingredient_id)
                )

            seen.add(ingredient_id)

    def check_ingredients_exist(self, ingredient_ids: List[int], dish_id: int):
        does_not_exist_error: str = (
            "Invalid ingredient_id '{ingredient_id}' - "
            "the specified dish does not have this ingredient."
        )

        existing_ingredients_ids: List[int] = \
            models.DishIngredients.objects.filter(
            ingredient_id__in=ingredient_ids, dish_id=dish_id
            ).values_list("ingredient_id", flat=True)

        if len(existing_ingredients_ids) != len(ingredient_ids):
            for ingredient_id in ingredient_ids:
                if ingredient_id not in existing_ingredients_ids:
                    raise ValidationError(
                        does_not_exist_error.format(
                            ingredient_id=ingredient_id
                        )
                    )
