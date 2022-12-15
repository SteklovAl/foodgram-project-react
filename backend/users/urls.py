from django.urls import include, path
from rest_framework import routers

from .views import FollowViewSet, SubscriptionsView

app_name = 'users'

router = routers.DefaultRouter()
router.register('users', FollowViewSet, basename='user')

urlpatterns = [
    path(
        'users/subscriptions/', SubscriptionsView.as_view(),
        name='subscriptions'
        ),
    path("", include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
