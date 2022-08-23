# IQoption API

### ToDo

- [x] Account Balance 
- [x] trade buy and sell "Digital & Turbo"
- [x] Check Win
- [x] check open Markets
- [x] remaning time
- [x] real time quote
- [x] ohlc dataframe history
- [x] payout


## Installation
#### Tested on python 3.7 to 3.9
```
pip install ejtraderIQ -U
```
#### Or install from source

```
git clone https://github.com/ejtraderLabs/ejtraderIQ
cd ejtraderIQ
python setup.py install

```

### Import librarys 

```python
from ejtraderIQ import IQOption

```

### Login to IQ Options

```python
# account type DEMO OR LIVE
api = IQOption('email','passowrd','DEMO') 

symbol = "EURUSD"
timeframe= "M1"
```
### Real time quote

##### Subscribe quote stream 
```python
api.subscribe(symbol,timeframe)
```
##### symbols quote  
```python
quote = api.quote()
print(quote)

# Output

                         open      high       low     close  volume
date                                                               
2022-08-22 22:39:00  0.994245  0.994415  0.994215  0.994365     120
```
##### Unsubscribe quote stream  
```python
api.unsubscribe(symbol,timeframe)

# Output
"Unsubscribed from EURUSD"
```

#### Symbols History Dataframe
```python
candles = 1000 # max history 1000 periods

history = api.history(symbol,timeframe,candles)
print(quote)

# Output
                         open      high       low     close  volume
date                                                               
2022-08-17 12:20:00  1.016235  1.016565  1.015925  1.016005    1225
2022-08-17 12:25:00  1.016015  1.016265  1.015585  1.016195     947
2022-08-17 12:30:00  1.016015  1.016905  1.014535  1.014635    3280
2022-08-17 12:35:00  1.014635  1.015415  1.014605  1.015315    1646
2022-08-17 12:40:00  1.015305  1.016015  1.015305  1.015985    1685
...                       ...       ...       ...       ...     ...
2022-08-22 23:15:00  0.993955  0.994035  0.993435  0.993475     779
2022-08-22 23:20:00  0.993475  0.993635  0.993365  0.993405     547
2022-08-22 23:25:00  0.993405  0.993585  0.993335  0.993455     577
2022-08-22 23:30:00  0.993475  0.993495  0.993305  0.993435     519
2022-08-22 23:35:00  0.993415  0.993655  0.993375  0.993635     527

[1000 rows x 5 columns]
```



##### Trade Position

```python
volume = 1 # position size $1


# Buy Digital
api.buy(volume,symbol,timeframe)

# Buy turbo
api.buy(volume,symbol,timeframe,turbo=True)

# Sell Digital
api.sell(volume,symbol,timeframe)

# Sell turbo
api.sell(volume,symbol,timeframe,turbo=True)

```



#### Trade & Account Fuctions

##### check Payout
```python

payout = api.payout(symbol) 
print(("Payout: {:.2f}%".format(payout)))
```
##### Check balance
```python
 balance = api.balance()
 print(f'Balance : {balance}')
```

##### Remaning tim to trade 
```python
 expire = api.remaning(timeframe)
 print(f'Remaning : {expire}')
```
##### Check Win
```python
api.checkwin(id)

# example check win
id = api.buy(volume,symbol,timeframe)
win = api.checkwin(id)

if win > 0:
    print(("WIN"+'\n'))
elif win < 0:                                            
    print(("LOSS"+'\n'))
else:
    print(('Tied '+'\n'))    
```

##### Check markets state
```python
markets = api.isOpen()
print(markets)

# Output

          Asset    Type Status
0    USDZAR-OTC  binary  close
1        EURUSD  binary  close
2    GBPJPY-OTC  binary  close
3        BTCUSD  binary  close
4        USDCHF  binary  close
..          ...     ...    ...
371    BNBUSD-L  crypto   open
372    VETUSD-L  crypto   open
373      ETCUSD  crypto   open
374   DOGEUSD-L  crypto   open
375    ETCUSD-L  crypto   open

[376 rows x 3 columns]

```


