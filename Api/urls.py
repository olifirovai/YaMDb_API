from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Api.views import UserViewSet, UserProfileView
from Api.utils import send_confirmation_code, get_token

router = DefaultRouter()
router.register('users', UserViewSet, 'users')
urlpatterns = [
    path('v1/users/me/', UserProfileView.as_view()),
    path('v1/auth/email/', send_confirmation_code, name='send_code'),
    path('v1/auth/token/', get_token, name='token'),
    path('v1/', include(router.urls)),

]
