from Api.models import User
from Api.serializers import UserSerializer
from rest_framework import viewsets, status
from Api.permissions import IsAdmin
from Api.utils import unique_confrm_code_generator
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.core.exceptions import PermissionDenied


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAuthenticated, IsAdmin,)

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

    def update(self, request, *args, **kwargs):
        user = get_object_or_404(User, email=request.data.get('email'),
                                 username=request.data.get('username'))
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if not request.data.get('role'):
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        raise PermissionDenied()
