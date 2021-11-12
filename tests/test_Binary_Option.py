import unittest
import os
from ejtraderIQ.stable_api import IQ_Option
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
 
email=os.getenv("email")
password=os.getenv("password")
class TestBinaryOption(unittest.TestCase):
  
    def test_binary_option(self):
        #login
        api=IQ_Option(email,password)
        api.change_balance("PRACTICE")
        api.reset_practice_balance()
        self.assertEqual(api.check_connect(), True)
        #start test binary option
        ALL_Asset=api.get_all_open_time()
        if ALL_Asset["turbo"]["EURUSD"]["open"]:
            ACTIVES="EURUSD"
        else:
            ACTIVES="EURUSD-OTC"
        Money=1
        ACTION_call="call"#or "put"
        expirations_mode=1
        check_call,id_call=api.buy(Money,ACTIVES,ACTION_call,expirations_mode)
        self.assertTrue(check_call)
        self.assertTrue(type(id_call) is int)
        api.sell_option(id_call)

        ACTION_call="put"
        check_put,id_put=api.buy(Money,ACTIVES,ACTION_call,expirations_mode)
        self.assertTrue(check_put)
        self.assertTrue(type(id_put) is int)
        api.sell_option(id_put)
        api.check_win_v2(id_put)
        
        
        api.get_binary_option_detail()

        api.get_all_profit()

        isSuccessful,dict=api.get_betinfo(id_put)
        self.assertTrue(isSuccessful)
        api.get_optioninfo(10)
  