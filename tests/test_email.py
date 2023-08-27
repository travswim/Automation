import unittest
from src.send_email import SendEmail


class TestSendEmail(unittest.TestCase):
    def setup(self):
        # TODO: Generate fake data for testing
        pass

    def teardown(self):
        pass

    def test_send_email(self):
        email = SendEmail()
        assert email.send_email('a', 'b', 'c', 'd') is True
