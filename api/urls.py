from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .utils import send_confirmation_code, get_token
from .views import (CategoryViewSet,
                    GenreViewSet,
                    TitleViewSet,
                    ReviewViewSet,
                    CommentViewSet,
                    UserViewSet,
                    UserProfileView
)

router = DefaultRouter()
router.register('users', UserViewSet, 'users')
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='review')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment')

urlpatterns = [
    path('v1/users/me/', UserProfileView.as_view()),
    path('v1/auth/email/', send_confirmation_code, name='send_code'),
    path('v1/auth/token/', get_token, name='token'),
    path('v1/', include(router.urls)),
]
