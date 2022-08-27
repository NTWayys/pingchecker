from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import re

# Create your views here.
from .serializers import serverListSerializer
from .utils import frontPage, domainTarget, updateServer, getServerDetail, deleteServer, getServerList, createServer


def index(request):
    return render(request, 'frontend/index.html', {'context': frontPage(request)})


def getDomain(request, domain):
    domain = domain.lower()
    if re.search("^((?!-))(xn--)?[a-z0-9][a-z0-9-_]{0,61}[a-z0-9]{0,1}\.(xn--)?([a-z0-9\-]{1,61}|[a-z0-9-]{1,30}\.[a-z]{2,})$", domain):
        return render(request, 'frontend/test.html', {'context': domainTarget(request, domain)})
    else:
        return render(request, 'frontend/test.html', {'context': {"notvalid": domain + " is not a valid domain, check for spaces or unique characters"}})


@api_view(['GET'])
def getRoutes(request):

    routes = [
        {
            'Endpoint': '/server/list/',
            'method': 'GET',
            'body': None,
            'description': 'returns the server list'
        },
        {
            'Endpoint': '/server/id/',
            'method': 'GET',
            'body': None,
            'description': 'returns target server'
        },
        {
            'Endpoint': '/server/id/update/',
            'method': 'PUT',
            'body': {'body': "JSON format"},
            'description': 'update target "id" server'
        },
        {
            'Endpoint': '/server/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'delete target "id" server'
        },
    ]
    return Response(routes)


@api_view(['GET'])
def getServers(request):
    return getServerList(request)


@api_view(['POST'])
def addServer(request):

    if request.method == 'POST':
        return createServer(request)


@api_view(['GET', 'PUT', 'DELETE'])
def updateServers(request, id):

    if request.method == 'GET':
        return getServerDetail(request, id)

    if request.method == 'PUT':
        return updateServer(request, id)

    if request.method == 'DELETE':
        return deleteServer(request, id)
