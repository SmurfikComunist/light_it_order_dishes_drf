from django.core.validators import MinValueValidator
from django.db import models


class Ingredient(models.Model):

    # Fields
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return str(self.name)


class Dish(models.Model):

    # Relationships
    ingredients = models.ManyToManyField(
        Ingredient, through="DishIngredients"
    )

    # Fields
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return str(self.name)


class DishIngredients(models.Model):

    # Relationships
    dish = models.ForeignKey(
        Dish, on_delete=models.CASCADE, related_name="dish_ingredients"
    )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    # Fields
    ingredients_amount = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return str(self.pk)


class Order(models.Model):

    # Relationships
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(
        Ingredient, through="OrderIngredients"
    )

    # Fields
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return str(self.pk)


class OrderIngredients(models.Model):

    # Relationships
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_ingredients"
    )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    # Fields
    ingredients_amount = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return str(self.pk)
