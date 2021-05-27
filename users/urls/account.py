from django.urls import path, include
from django.contrib.auth import views as auth_views
from users.views.account import register_view, notifications_view, mark_notification_as_seen

app_name = 'account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html')),
    path('', include('django.contrib.auth.urls')),
    path('register/', register_view, name='register'),
    path('social-auth/', include('social_django.urls')),
    path('notifications/', notifications_view, name='notifications'),
    path('notifications/mark-as-seen/<int:notification_id>/', mark_notification_as_seen, name='notifications_mark_as_seen'),
]
