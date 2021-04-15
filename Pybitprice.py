'''
Uso de API de COINBASE.com
Coinbase Inc. es una plataforma de comercio de criptomonedas con sede en San Francisco, California, que ofrece servicios
de intercambio entre criptomonedas y monedas fiduciarias en alrededor de 32 países, así como almacenamiento y gestión de
activos digitales en 190 países en todo el mundo.

API de coinbase, Obtiene precio Spot, Precios variables, formato Json
'''
import requests
from coinbase.wallet.client import Client

client = Client('https://api.coinbase.com/v2/currencies', '0')

def get_currency(cod):
    try:
        codCurrency = cod.upper()
        url_list = str('https://api.coinbase.com/v2/currencies')
        req = requests.get(url_list)
        currencyList = req.json()['data']
        for cod in currencyList:
            if codCurrency == cod['id']:
                currencyName = cod['name']
    except KeyError:
        print(req.json()['errors'][0]['message'])    
    return currencyName

def price_1(currency_code):
    try: 
        # can also use EUR, CAD, etc.        
        _apiKey = str('https://api.coinbase.com/v2/prices/spot?currency=') + currency_code
        # Make the request        
        r = requests.get(_apiKey)        
        nameCurrency = get_currency(currency_code)
        print('Bitcoin price in %s' % nameCurrency) 
        price = float(r.json()['data']['amount'])   # string amount se convierte a float          
        print(currency_code.upper(), f'{price:,.2f}', '\n') # se da formato de 2 decimales al precio
        Server_time()
    except KeyError:         
        print(r.json()['errors'][0]['message']) # mensaje de error cuando la moneda es invalida

def price_2():    
    Result0 = client.get_buy_price()
    Result1 = client.get_sell_price()
    Result2 = client.get_spot_price()    
    print('Compra {}/{}: '.format(Result2.base, Result2.currency), Result0.get('amount')) #uso 1 de .format
    print('Venta  {}/{}: '.format(Result2.base, Result2.currency), Result1.get('amount'))
    print('Spot   {}/{}: '.format(Result2.base, Result2.currency), Result2.get('amount'))
    print('Currency %s price in %s: %s' % ( Result2.base, Result2.currency, Result2.amount)) #uso 2 de .format
    

def price_now(cripto):
    # BTC = Bitcoin, BCH = Bitcoin Cash, BSV = Bitcoin SV, WBTC = Wrapped Bitcoin,
    # LTC = Litecoin, ETH = Ethereum, ETC = Ethereum Classic, DASH = Dash, EOS = Eos, AAVE = Aave, 
    # YFI = Yearn.finance, MKR = Maker    
    curr_par = (cripto + '-USD').upper()   
    print('Compra: USD ', client.get_buy_price(currency_pair = curr_par)['amount'])
    print('Venta:  USD ', client.get_sell_price(currency_pair = curr_par)['amount'])
    print('Spot:   USD ', client.get_spot_price(currency_pair = curr_par)['amount'])
    min_satoshi = float(client.get_currencies(id='USD')['data'][0]['min_size'])
    satoshi = float((client.get_spot_price(currency_pair = curr_par))['amount']) * min_satoshi * 144 #dolar 03/2021 -- 69.74 #dolar a 03/2020
    print(f'Satoshi price: ARS {satoshi:,.2f}')
    Server_time()

def Server_time():
    client = Client('https://api.coinbase.com/v2/time', '0')
    time = client.get_time()
    print('Server time: ', time.get('iso'))


print(' Seleccione: \n', '1. Por Tipo Moneda \n','2. Consulta Precio Bitcoin \n','3. Actualizado por Criptomoneda\n', 'Opcion: ', end='')
opcion = input()
if opcion == "1":
    currency = input("Inica un tipo de moneda:\n\t(USD, EUR, CAD, GBP, ARS, PYG, BRL, COP, VES, XAU (Gold - Troy Ounce)): ")
    price_1(currency)
elif opcion == '2':        
    price_2()
else:
    cripto = input("""Inica un tipo de criptomoneda: 
    \tBTC = Bitcoin\n\tBCH = Bitcoin Cash\n\tBSV = Bitcoin SV
    \tWBTC = Wrapped Bitcoin\n\tLTC = Litecoin\n\tETH = Ethereum 
    \tETC = Ethereum Classic\n\tDASH = Dash\n\tEOS = Eos\n\tCOMP = Compound
    \tAAVE = Aave\n\tYFI = Yearn.finance\n\tMKR = Maker\n\t\tOpcion: """)
    price_now(cripto)