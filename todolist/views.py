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

from todolist.models import Post

from django.contrib.auth import get_user_model
UserModel = get_user_model()
from django.core import serializers
from django.http import HttpResponse

@csrf_exempt
@api_view(["POST"])
def addEvent(request):
    title = request.data.get("title")
    text = request.data.get("description")
    tokenKey = request.META.get('HTTP_AUTHORIZATION').split()[1]
    userData = Token.objects.get(key=tokenKey)
    if title is None or text is None:
        return Response(
            {
                'status': 'false',
                'message': 'Please provide both title and description'
            },
            status=HTTP_400_BAD_REQUEST)

    todo =  Post.objects.create(
            author=UserModel.objects.get(id=userData.user_id),
            title=title,
            text=text
        )
    todo.save()
    return Response(
        {
            'status': 'true',
            'message': 'Successfully saved event'
        },
        status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def editEvent(request):
    eventId = request.data.get("eventId")
    title = request.data.get("title")
    text = request.data.get("description")
    tokenKey = request.META.get('HTTP_AUTHORIZATION').split()[1]
    userData = Token.objects.get(key=tokenKey)

    if eventId is None or title is None or text is None:
        return Response(
            {
                'status': 'false',
                'message': 'Please provide both title and description'
            },
            status=HTTP_400_BAD_REQUEST)
    eventId = Post.objects.get(id=eventId).id
    todo =  Post.objects.filter(
                    id = eventId
                ).update(
                    author=UserModel.objects.get(id=userData.user_id),
                    title=title,
                    text=text
                )
    return Response(
        {
            'status': 'true',
            'message': 'Successfully updated event'
        },
        status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def deleteEvent(request):
    eventId = request.data.get("eventId")

    if eventId is None:
        return Response(
            {
                'status': 'false',
                'message': 'Please provide id'
            },
            status=HTTP_400_BAD_REQUEST)
    eventId = Post.objects.get(id=eventId).id
    todo =  Post.objects.filter(
                    id = eventId
                ).delete()
    return Response(
        {
            'status': 'true',
            'message': 'Successfully deleted event'
        },
        status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
def listEvent(request):
    tokenKey = request.META.get('HTTP_AUTHORIZATION').split()[1]
    userData = Token.objects.get(key=tokenKey)
    userObj = UserModel.objects.get(id=userData.user_id)
    listData = Post.objects.filter(author=userObj)
    returnData = []
    for data in listData:
        item = {}
        item['id'] = data.id
        item['title'] = data.title
        item['description'] = data.text
        returnData.append(item)
    return Response(
        returnData,
        status=HTTP_200_OK)