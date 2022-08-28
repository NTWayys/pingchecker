from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import re

# Create your views here.
from .serializers import serverListSerializer
from .utils import domainTarget


def index(request):
    return render(request, 'frontend/index.html')


def getDomain(request, domain):
    domain = domain.lower()
    if re.search("^((?!-))(xn--)?[a-z0-9][a-z0-9-_]{0,61}[a-z0-9]{0,1}\.(xn--)?([a-z0-9\-]{1,61}|[a-z0-9-]{1,30}\.[a-z]{2,})$", domain):
        return render(request, 'frontend/test.html', {'context': domainTarget(domain)})
    else:
        return render(request, 'frontend/test.html', {'context': {"notvalid": domain + " is not a valid domain, check for spaces or unique characters"}})


@api_view(['GET'])
def getDomainFromAPI(request, domain):
    domain = domain.lower()
    if re.search("^((?!-))(xn--)?[a-z0-9][a-z0-9-_]{0,61}[a-z0-9]{0,1}\.(xn--)?([a-z0-9\-]{1,61}|[a-z0-9-]{1,30}\.[a-z]{2,})$", domain):
        return Response(domainTarget(domain))
    else:
        return Response({
            "address": domain,
            "status": domain + " is not a valid domain, check for spaces or unique characters",
            "notes": "Try removing any unique characters such as !@#$%^&*() which do not belong in a domain",
        }, status=status.HTTP_400_BAD_REQUEST)
