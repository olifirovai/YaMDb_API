import random
import string
from Api.models import User
from django.core.mail import send_mail
from Api.serializers import EmailSerializer, ConfirmationCodeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator

def random_code_generator(size=30,
                          chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_confrm_code_generator():
    confirmation_code = random_code_generator()
    qs_exists = User.objects.filter(
        confirmation_code=confirmation_code).exists()
    if qs_exists:
        return random_code_generator()
    return confirmation_code


@api_view(['POST'])
def send_confirmation_code(request):
    serializer = EmailSerializer(data=request.data)
    user = get_object_or_404(User, email=request.data['email'])
    if serializer.is_valid():
        token = default_token_generator.make_token(user)
        mail_subject = 'Confirmation code'
        message = f'Use this code:{token} to get your personal Token'
        send_mail(mail_subject, message, None , [user.email])
        return Response(f'Your confirmation code will be sent to your email: {user.email}',
                        status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_token(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    user = get_object_or_404(User, email=request.data['email'])
    if serializer.is_valid():
        if serializer.validated_data[
            'confirmation_code'] == user.confirmation_code:
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}', }, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
