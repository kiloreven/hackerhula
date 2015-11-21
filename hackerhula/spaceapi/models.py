from django.db import models

class RoomState(models.Model):
    roomname = models.CharField("Which room/area is concerned by this record?", max_length=255)
    is_open = models.BooleanField("Is the room open right now?", default=False)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Room %s (currently %s)" % (
            self.roomname, "open" if self.is_open else "closed")
