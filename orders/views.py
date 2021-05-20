import stripe
from django.conf import settings
from django.shortcuts import render, redirect, reverse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from stores.models import Pizza


# Create your views here.
@login_required
def order_view(request):
    cards = stripe.Customer.list_sources(
        request.user.stripe_customer.stripe_id,
        object='card',
        api_key=settings.STRIPE_SECRET_KEY,
    )

    return render(request, 'orders/orders.html', {
        'cards': cards
    })


@login_required
def pay_order(request):
    card_id = request.POST['card_id']
    if request.method != 'POST' and card_id:
        raise Http404('Method not allowed')

    site_domain = Site.objects.get_current().domain
    print('site_domain', site_domain)

    cart_data = request.session['cart']
    pizza_list = Pizza.objects.filter(id__in=cart_data.keys())
    total_price = sum([pizza.price * cart_data[str(pizza.id)] for pizza in pizza_list])

    payment_intent = stripe.PaymentIntent.create(
        amount=int(total_price) * 100,
        currency='RON',
        confirm=True,
        return_url='%s%s' % (site_domain, reverse('payments:process')),
        customer=request.user.stripe_customer.stripe_id,
        payment_method=card_id,
        api_key=settings.STRIPE_SECRET_KEY,
    )

    next_action = payment_intent.get('next_action', {})
    if 'redirect_to_url' in next_action:
        return redirect(next_action['redirect_to_url']['url'])

    return redirect(reverse('payments:process'))
