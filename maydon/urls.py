from django.urls import path
from django.urls import path, include

from .views import (register_user,api_for_stadium_owner_update,
                    api_view_field,api_for_admin,api_for_stadum_owner,
                    api_for_stadum_owner_create,api_for_stadum_brone)
urlpatterns = [
    path('register/', register_user, name='register'),
    path('api_view_field/', api_view_field, name='api_view_field'),
    path('api_for_admin/', api_for_admin, name='api_for_admin'),
    path('api_for_stadum_owner/', api_for_stadum_owner, name='api_for_stadum_owner'),
    path('api_for_stadum_owner_create/', api_for_stadum_owner_create, name='api_for_stadum_owner_create'),
    path('api_for_stadum_owner_id/<int:pk>/', api_for_stadium_owner_update, name='api_for_stadum_owner_update'),
    path('api_for_stadum_brone/', api_for_stadum_brone, name='api_for_stadum_brone'),
    path('api_for_stadum_brone/<int:pk>/', api_for_stadum_brone, name='api_for_stadum_brone_id'),
    
]