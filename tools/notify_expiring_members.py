#!/usr/bin/env python
# .- coding: utf-8 -.
"""
Notify expiring members.

Author: Lasse Karstensen <lasse.karstensen@gmail.com>, January 2016.

# CRONMARKER: 00 09 * * * cd $HOME/hackerhula/tools/ && $HOME/venv/bin/python notify_expiring_members.py --run
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

from member.models import Member, Membership

SMTPSERVER = "localhost"
EMAILTEXT = u"""Hei %(name)s.

Medlemsskapet ditt i Hackeriet går snart ut.

Om opplysningene i systemet stemmer, går medlemskapet ut %(end_date)s.

Informasjon om hvordan du kan fortsette å være medlem finnes på:

    https://hackeriet.no/membership/

-- 
Mvh,
hackerhula
"""


def send_notification(membership):
    body = EMAILTEXT % {"name": membership.member.name,
                        "end_date": membership.end_date
                       }
    body = body.encode("utf-8")

    msg = MIMEText(body)
    msg["Subject"] = u"Medlemsskap løper ut"
    msg["From"] = u"Hackeriet <styret@hackeriet.no>"

    if 1:
        msg["To"] = membership.member.email
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

    today = date.today()

    if 0:
        today = date(year=2016, month=01, day=9)
        logging.debug("Today set to: %s" % today)

    notification_schedule = [-14, -2, 5, 10]  # days before expiration.
    for membership in Membership.objects.all():
        #if not membership.valid():
        #    continue
        logging.debug("Considering member %s's membership %s" %
                      (membership.member, membership))

        if membership.running:
            logging.debug("Skipping continuous membership for %s" %
                          membership.member)
            continue

        if "invalid" in membership.member.email:
            logging.debug("Skipping membership with invalid email: %s" %
                          membership.member)
            continue

        notification_schedule = map(lambda x: membership.end_date +
                                    timedelta(days=x), notification_schedule)

        logging.debug("Notification schedule is: %s" % str(notification_schedule))
        if today in notification_schedule:
            logging.debug("Sending notification to %s." % membership.member.email)
            send_notification(membership)
        else:
            logging.debug("Nothing to do")
