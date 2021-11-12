import unittest
import os
from ejtraderIQ.stable_api import IQ_Option
import logging
import time
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
 
email=os.getenv("email")
password=os.getenv("password")
class TestCandle(unittest.TestCase):
  
    def test_Candle(self):
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

        api.get_candles(ACTIVES, 60, 1000, time.time())
        #realtime candle
        size="all"
        api.start_candles_stream(ACTIVES,size,10)
        api.get_realtime_candles(ACTIVES,size)
        api.stop_candles_stream(ACTIVES,size)

