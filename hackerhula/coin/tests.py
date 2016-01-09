from django.test import TestCase

from django.core.urlresolvers import reverse

class ViewTests(TestCase):
    def test_auth(self):
        for uri in [reverse("brusaccount")]:
            response = self.client.get(uri)
            self.assertEqual(response.status_code, 302)
