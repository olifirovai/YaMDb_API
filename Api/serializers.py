from rest_framework import serializers

from Api.models import User


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.ReadOnlyField()
    description = serializers.CharField()
    email = serializers.EmailField(read_only=True)


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'description', 'email')
