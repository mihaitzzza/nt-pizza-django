from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.forms import RegisterForm
from users.emails import send_register_email
from users.models import Notification


# Create your views here.
def register_view(request):
    if request.method == 'GET':
        form = RegisterForm()
    else:  # consider this is POST method only
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            send_register_email(user)
            return redirect(reverse('users:account:login'))

    return render(request, 'users/register.html', {
        'form': form
    })


@login_required
def notifications_view(request):
    # notifications = Notification.objects.filter(user=request.user, seen=False).all()
    notifications = Notification.objects.filter(user=request.user).all()

    return render(request, 'users/notifications.html', {
        'notifications': notifications
    })


@login_required
def mark_notification_as_seen(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id)
    notification.seen = True
    notification.save()

    return redirect(reverse('users:account:notifications'))
