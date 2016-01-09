from django.test import TestCase

class ViewTests(TestCase):
    def test_public_views(self):
        for uri in ["/hula/"]:
            response = self.client.get(uri)
            self.assertEqual(response.status_code, 200)
