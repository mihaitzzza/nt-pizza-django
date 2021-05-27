from django.contrib.auth import get_user_model
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from api.serializers import UsersSerializer, PizzaSerializer, StoresSerializer, IngredientSerializer
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from stores.models import Pizza, Store, Ingredient

AuthUserModel = get_user_model()


# class UsersViewSet(ViewSet):
#     def list(self, request):
#         users = AuthUserModel.objects.all()
#         serializer = UsersSerializer(users, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         user = AuthUserModel.objects.filter(id=pk).first()
#         print('user', user)
#         if not user:
#             return Response({
#                 'message': 'Resource not found'
#             }, status=404)
#
#         serializer = UsersSerializer(user)
#         return Response(serializer.data)

class UsersViewSet(ModelViewSet):
    queryset = AuthUserModel.objects.all()
    serializer_class = UsersSerializer


class PizzaViewSet(ModelViewSet):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer


class StoreViewSet(ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoresSerializer


class IngredientView(ViewSet):
    def create(self, request):  # POST method
        name = request.POST['name']

        try:
            ingredient = Ingredient(name=name)
            ingredient.save()
        except IntegrityError:
            return Response({
                'message': 'Ingredient already exists.'
            }, status=400)

        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data, status=200)
