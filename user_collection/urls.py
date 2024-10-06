from django.urls import path
from .views import FetchAllMovies, RegisterUser, UserCollection, CollectionDetailView, RequestCountView, \
    ResetRequestCountView

urlpatterns = [
    path('movies/', FetchAllMovies.as_view(), name='fetch-all-movies'),
    path('register/', RegisterUser.as_view(), name='register_user'),
    path('collection/', UserCollection.as_view(), name='user_collection'),
    path('collection/<uuid:collection_uuid>/', CollectionDetailView.as_view(), name='collection-detail'),
    path('request-count/', RequestCountView.as_view(), name='request_count'),
    path('request-count/reset/', ResetRequestCountView.as_view(), name='reset_request_count'),
]