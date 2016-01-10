#!/usr/bin/env python
# .- coding: utf-8 -.
"""
Notify nettlaug members that a new period is starting.

Author: Lasse Karstensen <lasse.karstensen@gmail.com>, January 2016.

# CRONMARKER: 00 08 21 mar,jun,sep,dec * cd $HOME/hackerhula/tools/ && $HOME/venv/bin/python notify_nettlaug.py -v --run
"""
import codecs
import smtplib
import sys
import os
import logging
from pprint import pprint
from datetime import date, timedelta
from email.mime.text import MIMEText

sys.path.append("../")
sys.path.append("../hackerhula")
os.environ['DJANGO_SETTINGS_MODULE'] = 'hackerhula.settings'

from member.models import Member

SMTPSERVER = "localhost"
EMAILTEXT = u"""Hei %(name)s.

Da er vi snart inne i en ny periode for Hackeriet sitt nettlaug.

Du får denne eposten fordi i systemet står du oppført som nettlaug-medlem. Om dette ikke stemmer ta kontakt.

Betaling er vanligvis på forhånd for tre måneder av gangen, betalt før starten av hvert kvartal. For tiden er månedsavgiften kr. 350 per rack unit.

Sum: 1050,- NOK
Kontonummer: 1254.62.08964 (kun nettlaug)
Melding: Nettlaug %(name)s
Ingen KID.

Det beste er om du setter opp automatisk trekk kvartalsvis, så slipper kassereren å logge inn i nettbanken så mange ganger.

Mer informasjon finnes i nettlaugwikien: https://projects.hackeriet.no/projects/fibernett/wiki

-- 
Mvh,
Hackeriet
"""


def send_notification(member):
    body = EMAILTEXT % {"name": member.name}
    body = body.encode("utf-8")

    msg = MIMEText(body)
    msg["Subject"] = u"Ny nettlaug-periode"
    msg["From"] = u"Hackeriet Nettlaug <styret@hackeriet.no>"
    if 0:
        msg["To"] = member.email
        msg["Cc"] = u"lasse.karstensen@gmail.com"
    else:
        msg["To"] = u"lasse.karstensen@gmail.com"

    if "--run" in sys.argv:
        s = smtplib.SMTP(SMTPSERVER)
        s.sendmail("styret@hackeriet.no", [msg["To"]], msg.as_string())
        s.quit()
    else:
        print "--run argument missing, not sending the following email:"
        print msg.as_string()


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('UTF8')
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout)

    if "-v" in sys.argv:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    for member in Member.objects.filter(nettlaug_member=True):
        logging.debug("Considering member %s" % member)

        if "invalid" in member.email:
            logging.debug("Skipping member with invalid email: %s" %
                          member)
            continue

        logging.debug("Sending notification to %s." % member)
        send_notification(member)
