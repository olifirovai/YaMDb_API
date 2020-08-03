from Api.models import User
from Api.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from Api.permissions import IsOwner
from rest_framework import status
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def dispatch(self, request, *args, **kwargs):
    #     if kwargs.get('pk') == 'current' and request.user:
    #         kwargs['pk'] = request.user.pk
    #
    #     return super(UserViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = (IsAdminUser, IsOwner)
        return [permission() for permission in permission_classes]
