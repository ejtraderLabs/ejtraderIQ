from ejtraderIQ import IQOption


api = IQOption('email','password','DEMO')


for _ in range(5):
   id = api.buy(1,'EURUSD','M1')
   win = api.checkwin(id)
   print(win)
