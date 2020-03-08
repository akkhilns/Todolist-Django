from django.shortcuts import render

from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response

from django.contrib.auth import get_user_model
UserModel = get_user_model()


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response(
            {
                'status': 'false',
                'message': 'Please provide both username and password'
            },
            status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response(
            {
                'status': 'false',
                'message': 'Invalid Credentials'
            },
            status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response(
            {
                'status': 'true',
                'first_name': user.first_name,
                'token': token.key
            },
            status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def signUp(request):
    email = request.data.get("email")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    password = request.data.get("password")

    if email is None or first_name is None or last_name is None or password is None:
        return Response(
            {
                'status': 'false',
                'message': 'Please provide both required fields'
            },
            status=HTTP_400_BAD_REQUEST)
    user = UserModel.objects.create(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
    user.set_password(password)
    user.save()
    return Response(
            {
                'status': 'true',
                'message': "User created Successfully"
            },
            status=HTTP_200_OK)