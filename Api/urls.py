from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Api.views import UserViewSet, CustomAuthToken

router = DefaultRouter()
router.register('users', UserViewSet, 'users')
urlpatterns = [
    path('v1/auth/token/', CustomAuthToken.as_view(), name='token_obtain'),
    # path(v1/auth/email/),
    path('v1/', include(router.urls)),
]
