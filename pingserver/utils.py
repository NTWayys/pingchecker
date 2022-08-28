from rest_framework.response import Response
from .models import server
from .serializers import serverListSerializer
import os
import requests
from datetime import datetime
from time import sleep
from .config import siteConfigData
siteURL = siteConfigData['url']


def createServer(domain):
    serializer = serverListSerializer(data={'address': domain}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)


def updateServer(data, id):
    item = server.objects.get(id=id)
    serializer = serverListSerializer(instance=item, data=data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


def domainTarget(domain):
    context = {}
    try:
        updateTargetDomain(domain)
        targetDomain = server.objects.get(address=domain)
        serverInfo = {'dateadded': targetDomain.dateadded,
                      'address': targetDomain.address,
                      'status': targetDomain.status,
                      'notes': targetDomain.notes.split(";")[0],
                      }
        context = serverInfo
    except:
        createServer(domain)
        updateTargetDomain(domain)
        targetDomain = server.objects.get(address=domain)
        serverInfo = {'dateadded': "This is the first time this domain has been added to the server therefor it won't have info prior to today",
                      'address': targetDomain.address,
                      'status': targetDomain.status,
                      'notes': targetDomain.notes.split(";")[0],
                      }
        context = serverInfo
    return context


def updateTargetDomain(domain):
    targetDomain = server.objects.get(address=domain)
    osrequest = os.popen("ping -n 1 " + targetDomain.address).read()
    if "TTL=" in osrequest:
        for sentence in osrequest.split(":"):
            if 'Average' in sentence:
                reply = targetDomain.address + \
                    " is online, " + sentence.strip("\n").strip()
                updateServer({"status":  reply}, targetDomain.id)
    elif "Destination host unreachable" in osrequest:
        reply = targetDomain.address + " is unreachable"
        updateServer({"status":  reply, "notes":  "Server was last down at " + str(
            datetime.now().replace(microsecond=0)) + " ; "+targetDomain.notes}, targetDomain.id)
    elif "could not find host" in osrequest:
        reply = osrequest
        updateServer({"status":  reply, "notes":  "Server was last down at " + str(
            datetime.now().replace(microsecond=0)) + " ; "+targetDomain.notes}, targetDomain.id)
    elif "Request timed out" in osrequest:
        reply = osrequest
        updateServer({"status":  reply, "notes":  "Server was last down at " + str(
            datetime.now().replace(microsecond=0)) + " ; "+targetDomain.notes}, targetDomain.id)


# this runs on a timer of 1 min, using from django_q.models import Schedule


def updateServerStatus():
    serverList = server.objects.all()
    for targetDomain in serverList:
        osrequest = os.popen("ping -n 1 " + targetDomain.address).read()
        if "TTL=" in osrequest:
            for sentence in osrequest.split(":"):
                if 'Average' in sentence:
                    reply = targetDomain.address + \
                        " is online, " + sentence.strip("\n").strip()
                    updateServer({"status":  reply}, targetDomain.id)
        elif "Destination host unreachable" in osrequest:
            reply = targetDomain.address + " is unreachable"
            updateServer({"status":  reply, "notes":  "Server was last down at " + str(
                datetime.now().replace(microsecond=0)) + " ; "+targetDomain.notes}, targetDomain.id)
        elif "could not find host" in osrequest:
            reply = osrequest
            updateServer({"status":  reply, "notes":  "Server was last down at " + str(
                datetime.now().replace(microsecond=0)) + " ; "+targetDomain.notes}, targetDomain.id)
        elif "Request timed out" in osrequest:
            reply = osrequest
            updateServer({"status":  reply, "notes":  "Server was last down at " + str(
                datetime.now().replace(microsecond=0)) + " ; "+targetDomain.notes}, targetDomain.id)
