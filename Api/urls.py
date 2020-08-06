from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Api.views import UserViewSet, CustomAuthToken
from Api.utils import send_confirmation_code, get_token
from rest_framework.authtoken import views
router = DefaultRouter()
router.register('users', UserViewSet, 'users')
urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/email/', send_confirmation_code, name='send_code'),
    path('v1/auth/token/', CustomAuthToken.as_view(), name='token'),
    # path('v1/auth/', include('djoser.urls')),

]
