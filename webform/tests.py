from django.test import TestCase


class WebformTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_form(self):
        json_message = """
        {
          "slug": "submit233187828727065",
          "jsExecutionTracker": "build-date-1705790819657=>init-started:1705894344840=>validator-called:1705894344843=>validator-mounted-true:1705894344843=>init-complete:1705894344844=>onsubmit-fired:1705894354821=>submit-validation-passed:1705894354827",
          "submitSource": "form",
          "buildDate": "1705790819657",
          "q4_whatKind": [
            "Loss Runs (Commercial only)"
          ],
          "q6_attention": "john@example.com",
          "q7_brokerid": "",
          "q8_clientid": "",
          "q9_policyid": "",
          "timeToSubmit": "9",
          "preview": "true",
          "validatedNewRequiredFieldIDs": {
            "new": 1
          },
          "path": "submit233187828727065"
        }
        """