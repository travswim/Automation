import unittest
from src.send_email import SendEmail


class TestSendEmail(unittest.TestCase):
    def test_send_email(self):
        email = SendEmail()
        assert email.send_email() is True
