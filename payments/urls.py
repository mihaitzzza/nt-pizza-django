from django.urls import path
from .views import list_cards, add_card, remove_card, process_payment, failed_process


app_name = 'payments'

urlpatterns = [
    path('cards/', list_cards, name='list_cards'),
    path('cards/add/', add_card, name='add_card'),
    path('cards/<str:stripe_card_id>/remove', remove_card, name='remove_card'),
    path('process/', process_payment, name='process'),
    path('process/failed/', failed_process, name='failed'),
]
