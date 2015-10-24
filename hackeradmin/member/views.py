
import json
from base64 import b64decode
from pprint import pprint
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from hackeradmin import settings
from models import Member, PhysicalAccess

@login_required
def memberlist(request):
    res = {}
    res["members"] = Member.objects.all()
    return render(request, "memberlist.html", res)

def dooraccess(request):
    accepted = False
    if request.user.is_authenticated():
        accepted = True

    elif 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2 and auth[0].lower() == "basic":
            username, pw = b64decode(auth[1]).split(':', 1)
            if username == getattr(settings, "DOORCLIENT_USER", None) and \
                pw == getattr(settings, "DOORCLIENT_PASSWORD", None):
                accepted = True

    if not accepted:
        response = HttpResponse()
        response.status_code = 401
        response['www-authenticate'] = 'basic realm="doorclient"'
        return response

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

