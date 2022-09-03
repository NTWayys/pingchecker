from rest_framework.response import Response
from .models import server
from .serializers import serverListSerializer
import os
import re
from math import ceil
from datetime import datetime


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
        targetDomain = server.objects.get(address=domain)
        serverInfo = {'dateadded': targetDomain.dateadded,
                      'address': targetDomain.address,
                      'statpings': targetDomain.statpings,
                      'rollingpings': targetDomain.rollingpings,
                      'downpings': targetDomain.downpings.split(";")[0],
                      'whoisdata': targetDomain.whoisdata,
                      }
        context = serverInfo
    except:
        createServer(domain)
        updateTargetDomain(domain)
        targetDomain = server.objects.get(address=domain)
        serverInfo = {'dateadded': "This is the first time this domain has been added to the server therefor it won't have info prior to today",
                      'address': targetDomain.address,
                      'statpings': targetDomain.statpings,
                      'rollingpings': targetDomain.rollingpings,
                      'downpings': targetDomain.downpings.split(";")[0],
                      'whoisdata': targetDomain.whoisdata,
                      }
        context = serverInfo
    return context


def updateTargetDomain(domain):
    targetDomain = server.objects.get(address=domain)
    osrequest = os.popen("ping -n 1 " + targetDomain.address).read()
    if "TTL=" in osrequest:
        for sentence in osrequest.split(" "):
            if 'time=' in sentence:
                reply = sentence.strip("\n").strip()
                updateServer({"rollingpings":  reply}, targetDomain.id)
    elif any(s in osrequest for s in ("Destination host unreachable", "could not find host", "Request timed out")):
        reply = osrequest
        updateServer({"rollingpings":  reply, "downpings":  "Server was last down at " + str(
            datetime.now().replace(microsecond=0)) + " ; "+targetDomain.downpings}, targetDomain.id)


# this runs on a timer of 1 min, using from django_q.models import Schedule


def updateServerStatus():
    serverList = server.objects.all()
    for targetDomain in serverList:
        osrequest = os.popen("ping -n 1 " + targetDomain.address).read()
        if "TTL=" in osrequest:
            for sentence in osrequest.split(" "):
                if 'time=' in sentence:
                    pingVal = re.sub("[^0-9]", "", sentence)
                    rollingpingsarr = targetDomain.rollingpings
                    rollingpingsarr.insert(0, int(pingVal))
                    if len(rollingpingsarr) > 60:
                        rollingpingsarr.pop()

                    avgPing = str(ceil(sum(rollingpingsarr) /
                                       len(rollingpingsarr)))
                    minPing = str(min(rollingpingsarr))
                    maxPing = str(max(rollingpingsarr))
                    updateServer(
                        {"rollingpings": rollingpingsarr, "statpings": "Minimum = " + minPing + "ms, Maximum = " + maxPing + "ms, Average = " + avgPing + "ms."}, targetDomain.id)
        elif any(s in osrequest for s in ("Destination host unreachable", "could not find host", "Request timed out")):
            reply = osrequest
            updateServer({"rollingpings":  rollingpingsarr, "downpings":  "Server was last down at " + str(
                datetime.now().replace(microsecond=0)) + " ; "+targetDomain.downpings}, targetDomain.id)
