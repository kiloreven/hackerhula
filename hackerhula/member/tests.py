from django.test import TestCase

from django.core.urlresolvers import reverse

class ViewTests(TestCase):
    def test_auth(self):
        for uri in [
                    # reverse("memberlist"),  # Needs proper login.
                    reverse("dooraccess"),
                    reverse("unixaccount"),
                    ]:
            response = self.client.get(uri)
            self.assertEqual(response.status_code, 401)
