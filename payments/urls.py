from django.urls import path
from .views import list_cards, add_card, remove_card


app_name = 'payments'

urlpatterns = [
    path('cards/', list_cards, name='list_cards'),
    path('cards/add/', add_card, name='add_card'),
    path('cards/<str:stripe_card_id>/remove', remove_card, name='remove_card'),
]
