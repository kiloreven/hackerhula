from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from functools import wraps

import stripe
from .forms import PayForm
from .models import *
from member.models import Member

stripe.api_key = settings.STRIPE_KEYS['secret_key']


def api_basic_auth(func):
    @wraps(func)
    def _decorator(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            authmeth, auth = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
            if authmeth.lower() == 'basic':
                import base64
                auth = base64.b64decode(auth.strip()).decode('utf-8')
                username, password = auth.split(':', 1)
                machines = Machine.objects.filter(name=username, key=password)
                if len(machines) > 0:
                    kwargs["machine"] = machines[0]
                    return func(request, *args, **kwargs)
        response = HttpResponse("Brusmaskins only!!1")
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm="brusmaskins only"'
        return response
    return _decorator


@api_basic_auth
def sell(request, machine):
    response = HttpResponse()

    if 'product' in request.GET and 'hash' in request.GET:
        product = request.GET['product']
        userhash = request.GET['hash']
        if product == "0":
            p = machine.product0
        elif product == "1":
            p = machine.product1
        elif product == "2":
            p = machine.product2
        elif product == "3":
            p = machine.product3
        elif product == "4":
            p = machine.product4

        member = Member.objects.get(access_card=userhash)
        transactions = Transaction.objects.filter(member=member.user)
        balance = transactions.aggregate(balance=models.Sum('value'))['balance']
        if balance >= p.price:
            t = Transaction(description="%s sold from %s" %
                                        (p.productname, machine.name),
				            member=member.user, machine=machine,
                            value=-p.price)
            t.save()
            response.write("Sold!")
        else:
            response.write("Insufficient funds")
            response.status_code = 400
    else:
        response.write("Mind your parameters")
        response.status_code = 400
    return response


@login_required
def account(request):
    uid = request.user.id
    transactions = Transaction.objects.filter(member=uid)
    balance = transactions.aggregate(balance=models.Sum('value'))

    res = {}
    res["history"] = transactions
    res["balance"] = balance["balance"]
    res["key"] = settings.STRIPE_KEYS['publishable_key']
    return render(request, "account.html", res)


@login_required
def charge(request):
    uid = request.user.id

    form = PayForm(request.POST)

    if form.is_valid():
        member = Member.objects.get(user=request.user)

        # TODO: Store this.
        customer = stripe.Customer.create(
            email=member.email,
            card=form.cleaned_data['stripeToken']
        )

        charge = stripe.Charge.create(
            customer=customer.id,
            amount=form.cleaned_data['amountt'],
            currency='NOK',
            description='Hackeriet'
        )

        t = Transaction(member=uid,
                        # Int. division on purpose,
                        value=(int(form.cleaned_data['amountt']) / 100),
                        description="Transfer with Stripe.")
        t.save()
        res = {}
        res["amount"] = int(form.cleaned_data['amountt'])/100

        return render(request, 'charge.html', res)
    return HttpResponse("Invalid request", status_code=400)
