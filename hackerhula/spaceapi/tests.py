from django.test import TestCase

class SpaceapiTests(TestCase):
    def test_public_views(self):
        for uri in [
                    "/hula/spaceapi/spaceapi.json"
                    #"/hula/spaceapi/open",
                    #"/hula/spaceapi/close",
                    ]:
            response = self.client.get(uri)
            self.assertEqual(response.status_code, 200)
