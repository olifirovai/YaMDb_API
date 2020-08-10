from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from Api.utils import unique_confrm_code_generator
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import (viewsets,
                            generics,
                            filters,
                            mixins,
                            status,
                            permissions
)
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Category, Genre, Title, Review, Comment, User
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,
                          ReviewSerialier,
                          CommentSerializer,
                          UserSerializer,
                          UserRoleSerializer
)
from .permissions import IsAdminOrReadOnly, IsAuthorOrAdminOrModerator, IsAdmin
from .filters import TitlesFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAuthenticated, IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = 'username'

    def perform_create(self, request):
        code = unique_confrm_code_generator()
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data.get('role', None):
                if serializer.validated_data['role'] == 'admin':
                    serializer.save(is_superuser=True, is_staff=True,
                                    confirmation_code=code)
                elif serializer.validated_data['role'] == 'moderator':
                    serializer.save(is_moderator=True,
                                    confirmation_code=code)
        serializer.save(confirmation_code=code)


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserRoleSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(GenericViewSet, ListModelMixin, CreateModelMixin,
                      DestroyModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name', ]
    lookup_field = 'slug'


class GenreViewSet(GenericViewSet, ListModelMixin, CreateModelMixin,
                   DestroyModelMixin):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerialier
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrAdminOrModerator,
    )
    pagination_class = PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        if Review.objects.filter(title=title,
                                 author=self.request.user).exists():
            raise ValidationError
        serializer.save(author=self.request.user, title=title)
        int_rating = Review.objects.filter(title=title).aggregate(Avg('score'))
        title.rating = int_rating['score__avg']
        title.save(update_fields=["rating"])

    def perform_update(self, serializer):
        serializer.save()
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        int_rating = Review.objects.filter(title=title).aggregate(Avg('score'))
        title.rating = int_rating['score__avg']
        title.save(update_fields=["rating"])


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrModerator,)
    pagination_class = PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
