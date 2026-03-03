from django.urls import path
from .views import EventsView, GroupsView, UsersView


urlpatterns = [
    path('events/', EventsView.as_view(), name='events'),
    path('groups/', GroupsView.as_view(), name='groups'),
    path('users/', UsersView.as_view(), name='users'),
]
