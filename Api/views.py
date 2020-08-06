from Api.models import User
from Api.serializers import UserSerializer, ConfirmationCodeSerializer
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser
from Api.permissions import IsOwner
from Api.utils import unique_confrm_code_generator
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from djoser.permissions import CurrentUserOrAdmin, CurrentUserOrAdminOrReadOnly
from rest_framework.authtoken.models import Token


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['role'] == 'admin':
                serializer.save(is_superuser=True, is_staff=True,
                                confirmation_code=unique_confrm_code_generator())
            elif serializer.validated_data['role'] == 'moderator':
                serializer.save(is_moderator=True,
                                confirmation_code=unique_confrm_code_generator())
            serializer.save(confirmation_code=unique_confrm_code_generator())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def dispatch(self, request, *args, **kwargs):
    #     if kwargs.get('id') == request.user.id:
    #         kwargs['pk'] = request.user.id
    #     return super(UserViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == 'destroy' or self.action == 'create':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = (IsOwner, IsAdminUser,)
        return [permission() for permission in permission_classes]


class CustomAuthToken(ObtainAuthToken):

    def post(request):
        serializer = ConfirmationCodeSerializer(data=request.data)
        user = get_object_or_404(User, email=request.data['email'])
        if serializer.is_valid():
            if serializer.validated_data[
                'confirmation_code'] == user.confirmation_code:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key, })
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
