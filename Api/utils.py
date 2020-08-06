import random
import string
from Api.models import User
from django.core.mail import send_mail
from Api.serializers import EmailSerializer, ConfirmationCodeSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
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
    email = request.data['email']
    mail_subject = 'Confirmation code'
    message = f'Use this code:{user.confirmation_code} to get your personal Token'
    if serializer.is_valid():
        send_mail(mail_subject, message, None , [email])
        return Response(f'Your confirmation code will be sent to your email: {email}',
                        status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_token(request):
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
