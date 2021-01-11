# -*- coding: utf-8 -*-

from binance.client import Client
import pandas as pd
import time


p= ['ETHUSDT','BTCUSDT','any other pair you want to trade']
c= ['ETH','BTC','any other']


# <<<<<TRAILING STOP LOSS >>>>> 
#==============================
def trailing():

    global point # You must to place this variable (point=0) in your code of buy.
                 # This is used to determine the buy price
    
    orders = client.get_open_orders(symbol= p)
    order= float(orders[0]['origQty'])

    fee= order * 0.0015

    fee_USDT= fee * point
    print('Fee USDT','{:.4f}'.format(fee_USDT))

    profit_min= fee_USDT * 2.5
    print('Mínimum profit', profit_min)

    minimum= point + profit_min
    
    while True:

        # Interval 5min
        candles= pd.DataFrame(client.get_klines(
            symbol= p,interval=Client.KLINE_INTERVAL_5MINUTE))
        candles= candles.sort_values(by=0,ascending=False)

        price= float(candles.loc[499][4])
        print('Actual price',price)

        low= float(min(candles.loc[499:493][3]))
        high= float(max(candles.loc[499:493][2]))

        dif= high - low
        print('Size of market','{:.2f}'.format(dif))

        if dif <= (price * 0.030):
            tsl= dif * 0.30
            print('tsl(30%)=','{:.4f}'.format(tsl))
        elif dif > (price * 0.030) and dif <= (price * 0.050):
            tsl= dif * 0.40
            print('tsl(40%)=','{:.4f}'.format(tsl))
        else:
            tsl= dif * 0.050
            print('tsl(50%)=','{:.4f}'.format(tsl))

        gain= price - point 
        print('pips of gain','{:.4f}'.format(gain))
        
        if price - tsl > minimum:

            stop_loss= price - tsl
            print('Stop_loss','{:.4f}'.format(stop_loss))

            dif_gain= 0
            
            if stop_loss > dif_gain:

                balance = client.get_asset_balance(asset= c)
                balance= float(balance['free'])
                
                if balance > 0:
                    
                    dif_gain= stop_loss

                    try:
                        orders= client.get_open_orders(symbol= p)
                        orderId= orders[0]['orderId']
                    except:
                        print('Nothing to sell')
                        break
                              
                    if orderId > 0:
                        
                        client.cancel_order(
                            symbol= p,
                            orderId= orderId)
                        
                        client.order_limit_sell(
                            symbol= p,
                            quantity= 10, 
                            price= stop_loss) # Adjust quantity to your desire
                        
                        print('Stop-loss increasing')    

                    else:                        
                        client.order_limit_sell(
                            symbol= p,
                            quantity= 10,
                            price= stop_loss) # Adjust quantity to your desire
                        
                        print('Stop-loss placed')
                else:
                    print('{} was selled succesfully'.format(p))
                    
                    # This value reset global variable to buy
                    point= 0                
                    #========================================

                    break
            else:
                time.sleep(3)
            
        else:
            print('Price is under profit level')
            time.sleep(10)   
