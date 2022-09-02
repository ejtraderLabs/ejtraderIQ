from .stable_api import IQ_Option
import logging
import time
from datetime import datetime
import pandas as pd
import os
from dateutil import tz

class IQOption:
    __version__ = "7.8.9.1"


    def __init__(self, email, password, account_type, verbose = False, checkConnection = False):
        self.email = email
        self.password = password
        self.account_type = account_type
        self.debug = verbose
        self.iq = None
        self.checkConnection = checkConnection


        if self.debug:
            logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')

        if self.iq == None:
            self.connect()
            


    def connect(self):
        print("Trying to connect to IqOption")
        self.iq = IQ_Option(self.email,self.password)
        self.iq.connect()


        if self.iq != None:
            while True:
                if self.iq.check_connect() == False:

                    print('Error when trying to connect')
                    print(self.iq)
                    print("Retrying")
                    self.iq.connect()
                else:
                    if not self.checkConnection:
                        print('Successfully Connected! Account type : ' + self.account_type)
                    break
                    time.sleep(3)
                if self.account_type == "DEMO":
                    self.iq.change_balance("PRACTICE") # PRACTICE or REAL
                    
                elif self.account_type == "REAL":
                    self.iq.change_balance("REAL") # PRACTICE or REAL


    
    def timeframe_to_seconds(self,timeframe):
        # Timeframe dictionary
        convert = {
            "S30": 30,
            "M1": 60,
            "M2": 120,
            "M3": 180,
            "M4": 240,
            "M5": 300,
            "M15": 900,
            "M30": 1800,
            "H1": 3600,
                
        }
        return convert[timeframe]   

    def timeframe_to_integer(self,timeframe):
        # Timeframe dictionary
        convert = {
            "S30": 1,
            "M1": 1,
            "M2": 2,
            "M3": 3,
            "M4": 4,
            "M5": 5,
            "M15": 15,
            "M30": 30,
            "H1": 60,
                
        }
        return convert[timeframe]

    def buy(self, contract, symbol, timeframe, turbo=None):
        timeframe = self.timeframe_to_integer(timeframe)
        if turbo:
            done, id = self.iq.buy(contract, symbol, "call", int(timeframe))
        else:
            done, id = self.iq.buy_digital_spot(symbol, contract, "call", int(timeframe))

        
        if not done:
            print('Error call')
            print(done, id)
            exit(0)
        
        return id


    def sell(self, contract, symbol, timeframe, turbo=None):
        timeframe = self.timeframe_to_integer(timeframe)
        if turbo:
            done, id = self.iq.buy(contract, symbol, "put", int(timeframe))
        else:
            done, id = self.iq.buy_digital_spot(symbol, contract, "put", int(timeframe))
        
        if not done:
            print('Error put')
            print(done, id)
            exit(0)
        
        return id   


    def trade(self, contract, symbol, timeframe, direction, turbo=None):
        timeframe = self.timeframe_to_integer(timeframe)
        if turbo:
            done, id = self.iq.buy(contract, symbol, direction, int(timeframe))
        else:
            done, id = self.iq.buy_digital_spot(symbol, contract, direction, int(timeframe))
        
        if not done:
            print('Error put')
            print(done, id)
            exit(0)
        
        return done, id   
    
    def balance(self):
        return self.iq.get_balance()

    def get_all_open_time(self):
        return self.iq.get_all_open_time()

    def isOpen(self):
        isOpen = []
        opened_market=self.iq.get_all_open_time()
        
        for type_name, data in opened_market.items():
            for Asset,value in data.items():
                if value['open'] == True:
                    value = 'open'
                else:
                    value = 'close'
                result = {
                "Asset": Asset,
                "Type" : type_name, 
                "Status" : value
                }
                isOpen.append(result)
            
        return pd.DataFrame(isOpen)

    def payout(self, symbol, turbo=None):
        if turbo:
            payout = self.iq.get_all_profit()
            payout = payout[symbol]['turbo']
        else:
            self.iq.subscribe_strike_list(symbol, 1)
            while True:
                data = self.iq.get_digital_current_profit(symbol, 1)
                if data:
                    payout = data
                    self.iq.unsubscribe_strike_list(symbol, 1)
                    break
        return payout

    def remaning(self, timeframe):
        t = self.timeframe_to_integer(timeframe)
        remaning_time=self.iq.get_remaning(t)
        purchase_time=remaning_time
        return purchase_time

    def checkwin(self,id,turbo=None):
        if turbo:
            win = self.iq.check_win_v3(id)
        else:
            if id !="error":
                while True:
                    check,win = self.iq.check_win_digital_v2(id)
                    if check==True:
                        break
    
        return win


    def powerbar_live(self, symbol):
        return self.iq.start_mood_stream(symbol)

    def powerbar_history(self, symbol):
        return self.iq.get_traders_mood(symbol)



    def history(self, symbol, timeframe,candles):
        timestamp = self.iq.get_server_timestamp()
        timeframe = self.timeframe_to_seconds(timeframe)
        

       
        x = self.iq.get_candles(symbol, int(timeframe), candles, timestamp)
        timestamp = int(x[0]["from"]) -1
        

        dataframe = pd.DataFrame(x)
        dataframe.sort_values(by=["from"], inplace=True, ascending=True)
        dataframe.drop(dataframe.tail(1).index, inplace=True)
        dataframe = dataframe.rename(columns = {'from': 'date', 'min': 'low','max':'high'})
        dataframe = dataframe.set_index(['date'])
        dataframe.index = pd.to_datetime(dataframe.index, unit='s')
        return dataframe[["open", "high", "low","close", "volume"]]



    def latest_candles(self, symbol, timeframe,candles):
        
        timeframe = self.timeframe_to_seconds(timeframe)
        

        
        timestamp = self.iq.get_server_timestamp()
        x = self.iq.get_candles(symbol, int(timeframe), candles, timestamp)
        timestamp = int(x[0]["from"])  - 1
        

        dataframe = pd.DataFrame(x)
        dataframe.sort_values(by=["from"], inplace=True, ascending=True)
        #dataframe.drop(dataframe.tail(1).index, inplace=True)
        dataframe = dataframe.rename(columns = {'from': 'date', 'min': 'low','max':'high'})
        dataframe = dataframe.set_index(['date'])
        dataframe.index = pd.to_datetime(dataframe.index, unit='s')
        return dataframe[["open", "high", "low","close", "volume"]]




    def subscribe(self,symbol,timeframe):
        timeframe = self.timeframe_to_seconds(timeframe)
        self.iq.start_candles_stream(symbol,int(timeframe),1)
        print("starting stream")
        time.sleep(0.5)
        self.vela = self.iq.get_realtime_candles(symbol,int(timeframe))

    def unsubscribe(self,symbol,timeframe):
        timeframe = self.timeframe_to_seconds(timeframe)
        self.iq.stop_candles_stream(symbol,int(timeframe))
        return f"Unsubscribed from {symbol} "

    def quote(self):
       
        for velas in  list(self.vela):
            date = self.vela[velas]["from"]
            open = self.vela[velas]["open"]
            high = self.vela[velas]["max"]
            low = self.vela[velas]["min"]
            close = self.vela[velas]["close"]
            volume = self.vela[velas]["volume"]
            data = [ date, open,  high,  low,  close, volume]

            df = pd.DataFrame ([data], columns = ['date','open','high','low','close','volume'])
        
            main = df.set_index(['date'])
            main.index = pd.to_datetime(main.index, unit='s')
        return main

    def get_candles(self,symbol,timeframe,interval):
        timestamp = self.iq.get_server_timestamp()
        return self.iq.get_candles(symbol,timeframe,interval,timestamp)


    def server_time(self):
        return self.timestamp_converter(
                    self.iq.get_server_timestamp()
                )
    

    def timestamp_converter(self,x):
        time = datetime.strptime(
            datetime.utcfromtimestamp(x).strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S"
        )
        return time   
        