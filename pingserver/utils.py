from rest_framework.response import Response
from .models import server
from .serializers import serverListSerializer
import os
import requests
from datetime import datetime
from time import sleep


def getServerList(request):
    items = server.objects.all()
    serializer = serverListSerializer(items, many=True)
    return Response(serializer.data)


def getServerDetail(request, id):
    items = server.objects.get(id=id)
    serializer = serverListSerializer(items, many=False)
    return Response(serializer.data)


def createServer(request, domain):
    print("createblock")
    serializer = serverListSerializer(data={'address': domain}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)


def updateServer(request, id):
    data = request.data
    item = server.objects.get(id=id)
    serializer = serverListSerializer(instance=item, data=data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


def deleteServer(request, id):
    item = server.objects.get(id=id)
    item.delete()
    return Response('Server was Removed!')


def frontPage(request):
    updateServerStatus()
    serverList = server.objects.all()
    context = []
    for domain in serverList:
        serverInfo = {'address': domain.address,
                      'status': domain.status,
                      'notes': domain.notes.split(";")[0],
                      }
        context.append(serverInfo)
    return context


def domainTarget(request, domain):
    context = {}
    try:
        updateTargetDomain(domain)
        domain = server.objects.get(address=domain)
        serverInfo = {'address': domain.address,
                      'status': domain.status,
                      'notes': domain.notes.split(";")[0],
                      }
        context = serverInfo
    except:
        createServer(request, domain)
        updateServerStatus()
        print("one")
        domain = server.objects.get(address=domain)
        serverInfo = {'address': domain.address,
                      'status': domain.status,
                      'notes': domain.notes.split(";")[0],
                      }
        context = serverInfo
    return context


def updateTargetDomain(domain):
    domainTarget = server.objects.get(address=domain)
    context = []
    osrequest = os.popen("ping -n 1 " + domainTarget.address).read()
    if "Destination host unreachable" in osrequest:
        reply = domainTarget.address + " is unreachable"
        requests.put('http://192.168.1.54:8000/server/' + str(domainTarget.id) + '/update/',
                     json={"status":  reply, "notes":  "Server was last down at " + str(datetime.now().replace(microsecond=0)) + " ; "+domainTarget.notes})
    elif "TTL=" in osrequest:
        for sentence in osrequest.split(":"):
            if 'Average' in sentence:
                reply = domainTarget.address + \
                    " is online, " + sentence.strip("\n").strip()
                updateServer()
                requests.put('http://192.168.1.54:8000/server/' + str(domainTarget.id) + '/update/',
                             json={"status":  reply})
    elif "could not find host" in osrequest:
        reply = osrequest
        requests.put('http://192.168.1.54:8000/server/' + str(domainTarget.id) + '/update/',
                     json={"status":  reply})


# this runs on a timer in models.py, reason for it being written a 2nd time is so I don't have to run non existing domains such as wayys.co.zsa
def updateServerStatus():
    serverList = server.objects.all()
    for domain in serverList:
        osrequest = os.popen("ping -n 1 " + domain.address).read()
        if "Destination host unreachable" in osrequest:
            reply = domain.address + " is unreachable"
            requests.put('http://192.168.1.54:8000/server/' + str(domain.id) + '/update/',
                         json={"status":  reply, "notes":  "Server was last down at " + str(datetime.now().replace(microsecond=0)) + " ; "+domain.notes})
        elif "TTL=" in osrequest:
            for sentence in osrequest.split(":"):
                if 'Average' in sentence:
                    reply = domain.address + \
                        " is online, " + sentence.strip("\n").strip()
                    requests.put('http://192.168.1.54:8000/server/' + str(domain.id) + '/update/',
                                 json={"status":  reply})
