from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.crypto import get_random_string
from datetime import timedelta
from rest_framework.response import Response
from rest_framework import status
import jwt
from django.conf import settings


def check_token(token):
    try:
        value = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return value
    except jwt.DecodeError:
        return Response({'error': 'DecodeError'}, status=status.HTTP_400_BAD_REQUEST)


def create_token(**kwargs):

    data = {
        **kwargs
    }
    try:
        token = jwt.encode(data, settings.SECRET_KEY, algorithm="HS256")
        return token
    except jwt.ExpiredSignatureError:
        return Response({'error': 'DecodeError'}, status=status.HTTP_400_BAD_REQUEST)
    
    


def get_register_url_for_refferal(request, token):
    protocol = request.scheme
    domain = get_current_site(request)
    refferal_link = reverse('user-reqister')
    return f"{protocol}://{domain}{refferal_link}?token={token}"
