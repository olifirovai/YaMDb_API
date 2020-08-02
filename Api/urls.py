from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView, )
from Api.views import UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, 'users')
urlpatterns = [
    path('v1/auth/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/', include(router.urls)),
]
