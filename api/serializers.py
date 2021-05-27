from django.contrib.auth import get_user_model
from rest_framework import serializers
from stores.models import Store, Pizza, Ingredient

AuthUserModel = get_user_model()


# class UsersSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     first_name = serializers.CharField()
#     last_name = serializers.CharField()
#     email = serializers.EmailField()
#     is_staff = serializers.BooleanField()
#     is_superuser = serializers.BooleanField()
#
#     def update(self, instance, validated_data):
#         pass
#
#     def create(self, validated_data):
#         pass


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUserModel
        exclude = ('password',)


class StoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        exclude = []


class PizzaStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('id', 'name', )


class PizzaSerializer(serializers.ModelSerializer):
    store = PizzaStoreSerializer()

    class Meta:
        model = Pizza
        exclude = []


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        exclude = []
