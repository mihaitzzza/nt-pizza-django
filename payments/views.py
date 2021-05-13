import stripe
from django.shortcuts import render, Http404, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from payments.models import StripeCard


@login_required
def list_cards(request):
    cards = stripe.Customer.list_sources(
        request.user.stripe_customer.stripe_id,
        object='card',
        api_key=settings.STRIPE_SECRET_KEY,
    )

    return render(request, 'payments/list_cards.html', {
        'cards': cards
    })


@login_required
def add_card(request):
    if request.method == 'POST':
        stripe_token = request.POST.get('stripeToken')

        if not stripe_token:
            raise Http404('stripeToken not provided')

        stripe_card = stripe.Customer.create_source(
            request.user.stripe_customer.stripe_id,
            source=stripe_token,
            api_key=settings.STRIPE_SECRET_KEY,
        )

        StripeCard(
            stripe_customer=request.user.stripe_customer,
            stripe_card_id=stripe_card['id']
        ).save()

        return redirect(reverse('payments:list_cards'))

    return render(request, 'payments/add_card.html', {
        'stripe_key': settings.STRIPE_PUBLIC_KEY
    })


@login_required
def remove_card(request, stripe_card_id):
    # Retrieve card from our DB.
    stripe_card = get_object_or_404(StripeCard, stripe_card_id=stripe_card_id)

    if request.method != 'POST' or stripe_card.stripe_customer.user.id != request.user.id:
        raise Http404('Method not allowed.')

    # Delete card on Stripe.
    stripe.Customer.delete_source(
        request.user.stripe_customer.stripe_id,
        stripe_card_id,
        api_key=settings.STRIPE_SECRET_KEY,
    )

    # Delete card from our DB.
    stripe_card.delete()

    return redirect(reverse('payments:list_cards'))