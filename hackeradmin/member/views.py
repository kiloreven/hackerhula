
import json
from pprint import pprint
from django.shortcuts import render
from django.http import HttpResponse

from models import Member, PhysicalAccess

def memberlist(request):
    res = {}
    res["members"] = Member.objects.all()
    return render(request, "memberlist.html", res)


def dooraccess(request):
    res = []
    for member in Member.objects.filter(active_membership=True):
        res += [{
            'contactinfo': "Member %s" % member.name,
            'access_token': member.access_card,
        }]

    for card in PhysicalAccess.objects.all():
        if not card.valid():   # XXX: Figure out how to do this more efficiently.
            continue
        res += [{
            'contactinfo': card.contactinfo,
            'access_token': card.access_token,
        }]

    return HttpResponse(json.dumps(res, indent=2), content_type="application/json")

