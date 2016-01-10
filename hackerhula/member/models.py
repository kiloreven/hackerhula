from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from pytz import utc

class Member(models.Model):
    memberid = models.IntegerField(help_text="Four digits, increasing from 1000.", unique=True)

    #user = models.ForeignKey(User, null=True)

    name = models.CharField(max_length=200)
    handle = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=500)
    picture = models.ImageField("Picture of member (keycard?).", blank=True)
    cellphone = models.CharField("Cellhone number)", max_length=200, blank=True)

    email = models.EmailField("Member email address")

    member_since = models.DateTimeField("Initially registered", auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    access_card = models.CharField(max_length=200, blank=True)

    unix_username = models.CharField(max_length=200, blank=True)
    unix_uid = models.IntegerField(null=True, blank=True)

    authorized_keys = models.TextField("SSH public keys", blank=True)

    hausmania_keynumber = models.IntegerField("Hausmania key serial number", null=True, blank=True)
    hausmania_deposit = models.BooleanField("Has key deposit been paid by member?", default=False)

    nettlaug_member = models.BooleanField(default=False)
    active_membership = models.BooleanField("Has the member an active membership?",
                                            help_text="The big knob. Disable if member is not active any more.", default=True)

    comment = models.TextField("Additional notes for this member.", blank=True)

    def has_unix_account(self):
        return self.unix_uid is not None

    def __unicode__(self):
        return u"[%i] %s aka %s (%s)" % (
            self.memberid, self.name, self.handle or "NOHANDLE",
            "active member" if self.active_membership else "dormant member")

class PhysicalAccess(models.Model):
    """
        Additional access cards.

        Envisioned use is access cards used for events and similar.

        Note that this is a list of cards, not a list of card-access-periods.
    """
    cardname = models.CharField("Short name/description of the card", max_length=200)
    contactinfo = models.CharField("Name and cellphone to person in charge of card",
        max_length=200)

    enabled = models.BooleanField("Is this access card enabled?", default=True,
        help_text="Only applies if within the described time frame.")

    access_token = models.CharField("Access token presented by card.",
        max_length=200, unique=True)

    access_start = models.DateTimeField("Card is valid starting from",
                                        default=datetime.utcnow)
    access_end = models.DateTimeField("Card is valid until")

    description = models.TextField("Additional notes", blank=True)

    def __unicode__(self):
        return "Access card %s managed by %s" % \
            (self.cardname, self.contactinfo)

    def valid(self):
        "Should the access card be granted access right now?"
        now = datetime.now(utc)

        if not self.enabled:
            return False
        if self.access_start > now or self.access_end < now:
            return False

        return True


class Membership(models.Model):
    """
    Memberships are:
        * Tied to a specific Member.
        * Can be discontinuous, as members forget to pay or have other priorities for a year.

    To discern if a valid membership is present, we will simply look for a paid
    one that covers the current date.

    """
    member = models.ForeignKey(Member)
    added_at = models.DateTimeField("When the membership entry was first added",
                                    auto_now_add=True)
    changed_at = models.DateTimeField("When was the membership entry last changed.",
                                    auto_now=True)
    paid = models.BooleanField("Has this membership been paid?", default=True)
    paid = models.BooleanField("Has this membership been paid?", default=True)

    start_date = models.DateField("Membership start date", auto_now_add=True)
    running = models.BooleanField("This membership is continuous", default=False)
    end_date = models.DateField("Membership end date. NOOP if is continuous.", null=True)

    description = models.TextField("Additional notes", blank=True)

    def __unicode__(self):
        return "<Membership for %s expiring %s>" % \
               (self.member.name, self.end_date)

    def valid(self, ts=None):
        "Is this Membership valid right now?"
        if ts is None:
            ts = datetime.now(utc)
        if not self.paid:
            return False

        if self.start_date > ts:
            return False

        if self.running is True:
            return True

        # If it isn't continuous, it needs an end date to be valid.
        if self.running is False and self.end_date is None:
            return False

        if self.end_date < ts:
            return False

        return True
