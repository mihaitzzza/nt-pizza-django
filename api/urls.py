from django.urls import path
from rest_framework_simplejwt import views
from rest_framework.routers import DefaultRouter
from api.views import UsersViewSet, PizzaViewSet, StoreViewSet, IngredientView


api_router = DefaultRouter()
# api_router.register('users', UsersViewSet, basename='users')  # use basename for simple ViewSet
api_router.register('users', UsersViewSet)  # basename not required for ModelViewSet
api_router.register('pizza', PizzaViewSet)
api_router.register('stores', StoreViewSet)
api_router.register('ingredients', IngredientView, basename='ingredients')

# Resource name: users
# [GET] /users/ -> get a list of all users
# [GET] /users/:id/ -> get a user by id
# [POST] /users/ -> create a new resource
# [PUT] /users/:id/ -> update user by id
# [DELETE] /users/:id/ -> delete user by id
urlpatterns = [
    path('auth/token/', views.TokenObtainPairView.as_view()),
    path('auth/refresh-token/', views.TokenRefreshView.as_view()),
] + api_router.urls
