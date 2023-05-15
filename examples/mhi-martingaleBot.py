from ejtraderIQ import IQOption
import time

def stop_profit_loss(profit, stop_gain, stop_loss):
    if profit <= float('-' + str(abs(stop_loss))):
        print('\nStop Loss hit!')
        exit()
    if profit >= stop_gain:
        print('\nStop Gain hit!')
        exit()

def Martingale(entry_value, payout):
    return round(entry_value * 2.2, 2)

api = IQOption('email', 'password', 'DEMO') # DEMO OR REAL

# Parameters
pair = "EURUSD" # or "EURUSD-OTC"
timeframe = "M1"
operation = 1  # 1 for "Digital", 2 for "Turbo"
entry_value_b = 1
stop_gain = 100
stop_loss = 30
martingale = 2
profit = 0
mhi_type = 1  # 1 for "MHI", 2 for "MHI2"
enter = True

while True:
    if enter:
        print('\n\nStarting operation!')
        direction = False
        print('Checking colors...', end='')
        
        candles = api.history(pair, timeframe, 3)
        
        candles_colors = ['g' if candle['open'] < candle['close'] else 'r' 
                          if candle['open'] > candle['close'] else 'd' 
                          for _, candle in candles.iterrows()]

        colors = ' '.join(candles_colors)
        print(colors)

        if colors.count('g') > colors.count('r') and colors.count('d') == 0 : direction = ('put' if mhi_type == 1 else 'call')
        if colors.count('r') > colors.count('g') and colors.count('d') == 0 : direction = ('call' if mhi_type == 1 else 'put')

        if direction:
            print('Direction:', direction)

            entry_value = entry_value_b
            for i in range(martingale):
                
                id = (api.buy(entry_value, pair, timeframe, turbo=True) 
                      if operation == 2 
                      else api.buy(entry_value, pair, timeframe))

                win = api.checkwin(id)

                if win is not None:
                    value = win if win > 0 else float('-' + str(abs(entry_value)))
                    profit += round(value, 2)

                    print('Trade result: ', end='')
                    print('WIN /' if value > 0 else 'LOSS /' , round(value, 2) ,'/', round(profit, 2),('/ '+str(i)+ ' GALE' if i > 0 else '' ))

                    entry_value = Martingale(entry_value, api.payout(pair))

                    stop_profit_loss(profit, stop_gain, stop_loss)

                    if value > 0 : break

                else:
                    print('\nERROR IN TRADE EXECUTION\n\n')

    time.sleep(0.5)
