from django.urls import path
from .views import SubscribeView, unsubscribe, send_mail_view

urlpatterns = [
    # path('', subscribe),
    path('', SubscribeView.as_view()),
    path('unsubscribe/', unsubscribe),
    path('sendmail/', send_mail_view),
]