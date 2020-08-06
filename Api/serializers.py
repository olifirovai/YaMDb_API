from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from Api.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = (
        'first_name', 'last_name', 'username', 'bio', 'email', 'role')

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    # class Meta:
    #     model = User
    #     fields = ('email', 'confirmation_code')
    #

class ConfirmationCodeSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)


    # class Meta:
    #     model = User
    #     fields = ('email', 'confirmation_code')
    #
