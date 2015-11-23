
import json
from base64 import b64decode
from pprint import pprint
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from hackerhula import settings
from models import Member, PhysicalAccess

@login_required
def memberlist(request):
    res = {}
    res["members"] = Member.objects.all()
    return render(request, "memberlist.html", res)


def authscreen():
    response = HttpResponse("Unauthorized", status=401)
    response['www-authenticate'] = 'basic realm="restricted"'
    return response


# Rewrite into a decorator.
def basicauth(request):
    accepted = False
    if request.user.is_authenticated():
        accepted = True

    elif 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2 and auth[0].lower() == "basic":
            username, pw = b64decode(auth[1]).split(':', 1)
            if username == getattr(settings, "APICLIENT_USER", None) and \
                pw == getattr(settings, "APICLIENT_PASSWORD", None):
                accepted = True
    return accepted


def dooraccess(request):
    if not basicauth(request):
        return authscreen()

    res = []
    default_expiry = datetime.today() + timedelta(days=30)
    for member in Member.objects.filter(active_membership=True):
        if len(member.access_card) == 0:
            continue
        res += [{
            'contactinfo': "Member %s" % member.name,
            'access_token': member.access_card,
            'expires': default_expiry.isoformat()
        }]

    for card in PhysicalAccess.objects.all():
        if not card.valid():   # XXX: Figure out how to do this more efficiently.
            continue
        res += [{
            'contactinfo': card.contactinfo,
            'access_token': card.access_token,
            'expires': card.access_end.isoformat()
        }]

    return HttpResponse(json.dumps(res, indent=2), content_type="application/json")

def unixaccount(request):
    if not basicauth(request):
        return authscreen()

    res = []
    for member in Member.objects.filter(active_membership=True):
        if member.unix_uid is None or len(member.unix_username) == 0:
            continue
        if len(member.authorized_keys) == 0:
            continue
        # Outputting the key string verbatim is done on purpose. Systems should
        # do their own checks.
        res += [{
            'name': member.name,
            'username': member.unix_username,
            'uid': member.unix_uid,
            'authorized_keys': member.authorized_keys,
            'last_modified': member.last_modified.isoformat(),
        }]

    return HttpResponse(json.dumps(res, indent=2), content_type="application/json")
