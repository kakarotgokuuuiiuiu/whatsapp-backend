from django.urls import path
from chat.views import unique_users, get_messages, get_messages_by_user, send_message, update_message_status

urlpatterns = [
    path('users/', unique_users),
    path('messages/', get_messages),
    path('messages/<str:wa_id>/', get_messages_by_user),
    path('send_message/', send_message),
    path('update_status/', update_message_status),  # <-- NEW endpoint for status update
]
