from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CategoryViewSet,
                    GenreViewSet,
                    TitleViewSet,
                    ReviewViewSet,
                    CommentViewSet,
                    UserViewSet, AuthEmailConfirmation
                    )

router = DefaultRouter()
router.register('auth', AuthEmailConfirmation, 'auth')
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
    path('v1/', include(router.urls)),
]
