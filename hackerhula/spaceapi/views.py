from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

import json

from .models import RoomState

def spaceapi(request):
    try:
        hackeriet = RoomState.objects.get(roomname="Hackeriet")
    except RoomState.DoesNotExist:
        # This single default entry doesn't warrant a separate fixture by
        # itself. Add it on the first load instead.
        hackeriet = RoomState(roomname="Hackeriet")
        hackeriet.save()

    res = {
        "api": "0.13",
        "space": "Hackeriet Oslo",
        "logo": "https://hackeriet.no/comotion-sjn-transparent-1.2.svg",
        #"logo": "http://comotion.hackeriet.no/logo/zha.png",
        "url": "https://hackeriet.no",
        "location": {
            "address": "Hausmannsgate 34, N-0182 Oslo, Norway",
            "lon": 10.753475,
            "lat": 59.919293
        },
        "contact": {
            "email": "styret@NOSPAM__hackeriet.no",
            "irc": "irc://irc.freenode.net/#oslohackerspace",
            "twitter": "@hackeriet"
        },
        "issue_report_channels": [
            "email"
        ],
        "projects": [ "https://hackeriet.no/projects/", ],
        "state": {
            # Switch this when we get the update mechanism going.
            #"open": hackeriet.is_open,
            #"lastchange": hackeriet.last_updated.strftime("%S"),
            "open": True,
            "message": "Usually open Tuesday evening and Saturdays. See web page or IRC for details."
        }
    }
    return HttpResponse(json.dumps(res, indent=2), content_type="application/json")

def open(request, roomname):
    room = get_object_or_404(RoomState, roomname)
    room.is_open = True
    room.save()
    return HttpResponse("OK")

def close(request, roomname):
    room = get_object_or_404(RoomState, roomname)
    room.is_open = False
    room.save()
    return HttpResponse("OK")
