from Api.models import User
from Api.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from Api.permissions import IsOwner

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, IsOwner)
