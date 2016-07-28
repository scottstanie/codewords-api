from django.test import TestCase, Client
import json

# Create your tests here.

def verify_json(response):
        """
        Function for verifying json.
        """
        try:
            json_object = json.loads(response)
        except ValueError, e:
            return False
        return True

class RouteTest(TestCase):
    def setUp(self):
        """
        Sets up client for tests.
        """
        self.client = Client()

    def test_ping(self):
        """
        Goes to /ping/ and checks for 'ping' message with status 200.
        """
        print "\nAccessing /ping/"
        response = self.client.get('/ping/')
        print "Status Code: %d" % response.status_code
        print "Page response: %s" % response.content
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "OK")

    def test_404(self):
        """
        Goes to /404/ and checks for status 404.
        """
        print "\nAccessing /404/"
        response = self.client.get('/404/')
        print "Status Code: %d" % response.status_code
        print "Page response: %s" % response.content
        self.assertEqual(response.status_code, 404)

    def test_json(self):
        """
        Goes to /api/ and checks for json.
        """
        print "\nAccessing /api/"
        response = self.client.get('/api/?format=json')
        print "Page response: %s" % response.content
        verify_response = verify_json(response.content)
        self.assertEqual(verify_response, True)
