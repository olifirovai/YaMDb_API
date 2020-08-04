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

'''Пока не Копируй'''
class TokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, attrs):
        email = {'email': attrs.get('email')}
        confirmation_code = {
            'confirmation_code': attrs.get('confirmation_code')}
        if not email.values():
            raise ValueError('Email is required.')
        elif not confirmation_code.values():
            raise ValueError('Confirmation code is required.')
        return self.is_valid()

    class Meta:
        model = User
        fields = ('email', 'confirmation_code')

