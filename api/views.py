from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleReadSerializer, TitleWriteSerializer,
                             ReviewSerializer, CommentSerializer,
                             UserSerializer, UserRoleSerializer,
                             EmailSerializer, CodeSerializer)
from content.filters import TitlesFilter
from content.models import Category, Genre, Title, Review, Comment
from user.models import User
from user.permissions import (IsAdminOrReadOnly, IsAuthorOrAdminOrModerator,
                              IsAdmin)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAuthenticated, IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = 'username'

    @action(methods=['get', 'patch', ], detail=False,
            permission_classes=(IsAuthenticated,),
            url_path='me')
    def user_profile(self, request):
        user = get_object_or_404(User, id=request.user.id)
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = UserRoleSerializer(user, data=request.data,
                                            partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class AuthEmailConfirmation(viewsets.ModelViewSet):
    @action(methods=['post'], detail=False, url_path='email')
    def send_confirmation_code(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, create = User.objects.get_or_create(
            email=serializer.validated_data.get('email'))
        if create:
            user.username = serializer.validated_data.get('email')
            user.save()
        token = default_token_generator.make_token(user)
        mail_subject = 'Confirmation code'
        message = f'Use this code:{token} to get your personal Token'
        send_mail(mail_subject, message, None, [user.email], )
        return Response(
            f'Your confirmation code will be sent to your email: {user.email}',
            status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='token')
    def get_token(self, request):
        serializer = CodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, email=serializer.validated_data.get(
            'email'))
        code = serializer.validated_data.get('code')
        if default_token_generator.check_token(user, code):
            token = RefreshToken.for_user(user)
            return Response({'token': f'{token.access_token}'},
                            status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer

    def get_queryset(self):
        return Title.objects.annotate(
            rating=Avg('titles_reviews__score')).all().order_by('name')


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrAdminOrModerator, ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        queryset = Review.objects.filter(title=title)
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrModerator,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'],
                                   title__id=self.kwargs['title_id'])
        queryset = Comment.objects.filter(review=review)
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'],
                                   title__id=self.kwargs['title_id'])
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user, review=review)
