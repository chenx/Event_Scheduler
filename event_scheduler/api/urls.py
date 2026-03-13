from django.urls import path
from .views import EventList, EventDetail, GroupList, UserList
# from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('events/', EventList.as_view(), name='events'),
    path("events/<int:pk>/", EventDetail.as_view(), name="event"),
    path('groups/', GroupList.as_view(), name='groups'),
    path('users/', UserList.as_view(), name='users'),
    # path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
