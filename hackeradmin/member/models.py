from django.db import models
from datetime import datetime

class Member(models.Model):
    memberid = models.IntegerField(help_text="Four digits, increasing from 1000.", unique=True)
    name = models.CharField(max_length=200)
    handle = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=500)
    picture = models.ImageField("Picture of member (keycard?).", blank=True)

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

    def __str__(self):
        return "[%i] %s aka %s (%s)" % (
            self.memberid, self.name, self.handle or "NOHANDLE",
            "active member" if self.active_membership else "dormant member")


#class Membership(models.Model):
#    start_date = models.DateTimeField("Membership start date")
#    running = models.BooleanField("This membership is continous")
#    end_date = models.DateTimeField("Membership end date")
