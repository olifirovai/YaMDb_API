from Api.models import User
from Api.serializers import UserSerializer, TokenSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from Api.permissions import IsOwner
from rest_framework import status
from Api.utils import unique_confrm_code_generator
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

'''Изменена - Копируй'''


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['role'] == 'admin':
                serializer.save(is_superuser=True, is_staff=True, confirmation_code=unique_confrm_code_generator())
            elif serializer.validated_data['role'] == 'moderator':
                serializer.save(is_moderator=True, confirmation_code=unique_confrm_code_generator())
            serializer.save(confirmation_code=unique_confrm_code_generator())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def dispatch(self, request, *args, **kwargs):
    #     if kwargs.get('pk') == 'current' and request.user:
    #         kwargs['pk'] = request.user.pk
    #
    #     return super(UserViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == 'destroy' or self.action == 'create':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = (IsAdminUser, IsOwner)
        return [permission() for permission in permission_classes]



'''Пока не Копируй'''
class CustomAuthToken(ObtainAuthToken):
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = TokenSerializer(data=request.data)
        user = get_object_or_404(User, email=request.data['email'])
        if serializer.is_valid():
            if serializer.validated_data['confirmation_code'] == user.confirmation_code:
                serializer.is_valid(raise_exception=True)
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key,})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)