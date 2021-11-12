import unittest
import os
from ejtraderIQ.stable_api import IQ_Option

email=os.getenv("email")
password=os.getenv("password")
class TestLogin(unittest.TestCase):
  
    def test_login(self):
        api=IQ_Option(email,password)
        api.change_balance("PRACTICE")
        api.reset_practice_balance()
        self.assertEqual(api.check_connect(), True)
         
  