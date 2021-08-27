from django import forms
from django.contrib import admin

from . import models


class IngredientAdminForm(forms.ModelForm):
    class Meta:
        model = models.Ingredient
        fields = "__all__"


class IngredientAdmin(admin.ModelAdmin):
    form = IngredientAdminForm
    list_display = [
        "name",
        "created_at",
        "updated_at",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]


class DishAdminForm(forms.ModelForm):
    class Meta:
        model = models.Dish
        fields = "__all__"


class DishIngredientsInline(admin.TabularInline):
    model = models.Dish.ingredients.through


class DishAdmin(admin.ModelAdmin):
    form = DishAdminForm
    list_display = [
        "name",
        "created_at",
        "updated_at",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]
    inlines = [DishIngredientsInline]


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = "__all__"


class OrderIngredientsInline(admin.TabularInline):
    model = models.Order.ingredients.through


class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm
    list_display = [
        "dish",
        "created_at",
        "updated_at",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]
    inlines = [OrderIngredientsInline]


admin.site.register(models.Ingredient, IngredientAdmin)
admin.site.register(models.Dish, DishAdmin)
admin.site.register(models.Order, OrderAdmin)
