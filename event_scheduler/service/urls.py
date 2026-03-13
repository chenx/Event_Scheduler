from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('events/', views.events, name='events'),
    path('events/<int:owner_id>', views.events_for_owner, name='events_for_owner'),
    path('event/<int:event_id>/', views.event, name='event'),
    path('datastore/', views.datastore, name='datastore'),
    path('save-item/', views.save_data_view, name='save_item'),
    path('delete-item/', views.delete_data_view, name='delete_item'),
    path('save-datastore-item/', views.save_datastore_view, name='save_datastore_item'),
    path('delete-datastore-item/', views.delete_datastore_view, name='delete_datastore_item'),
    path('delete-all-datastore-item/', views.delete_all_datastore_view, name='delete_all_datastore_view'),
    path('datastores/', views.DatastoreList.as_view(), name='datastores'),
]