from django.db import models

class Member(models.Model):
    memberid = models.IntegerField()
    name = models.CharField(max_length=200)
    handle = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=500)

    email = models.EmailField("Member email address")

    member_since = models.DateTimeField("initially registered")
    access_card = models.CharField(max_length=200)

    unix_username = models.CharField(max_length=200, blank=True)
    unix_uid = models.IntegerField(blank=True)

    authorized_keys = models.TextField("SSH public keys")

    hausmania_keynumber = models.IntegerField("Hausmania key serial number", blank=True)
    hausmania_deposit = models.BooleanField("Has Hausmania key deposit been paid?", default=False)

    nettlaug_member = models.BooleanField(default=False)

    comment = models.TextField("Additional notes for this member.")

    def has_unix_account(self):
        return self.unix_uid is not None

    def __str__(self):
        return "<Member \"%s(%s)\">" % (self.name, self.handle or "NOHANDLE")

class Membership(models.Model):
    start_date = models.DateTimeField("Membership start date")
    running = models.BooleanField("This membership is continous")
    end_date = models.DateTimeField("Membership end date")
