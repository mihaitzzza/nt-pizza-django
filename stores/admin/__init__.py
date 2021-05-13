from django.contrib import admin
from stores.models import Pizza, Ingredient, StoreIngredients
from stores.admin.store import StoreAdmin
from stores.models import Store, PizzaIngredients


class PizzaIngredientAdmin(admin.TabularInline):
    model = PizzaIngredients
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print('db_field.name', db_field.name)
        if not request.user.is_superuser and db_field.name == 'store_ingredient':
            kwargs['queryset'] = StoreIngredients.objects.filter(store__owner=request.user)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    inlines = (PizzaIngredientAdmin,)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and db_field.name == 'store':
            kwargs['queryset'] = Store.objects.filter(owner=request.user)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(StoreIngredients)
class StoreIngredientAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if not request.user.is_superuser:
            return queryset.filter(store__owner=request.user)

        return queryset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and db_field.name == 'store':
            kwargs['queryset'] = Store.objects.filter(owner=request.user)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
