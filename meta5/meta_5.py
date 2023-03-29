from pymongo import MongoClient
import MetaTrader5 as mt5
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime

user_1 = {
    'user_1': 22014542,
    'password': 'duzftxd8',
    'server': 'Deriv-Demo'
}

user_2 = {
    'user': 51135132,
    'password': 'yym2fmut',
    'server': 'ICMarketsEU-Demo'
}

user_3 = {
    'user': 51135134,
    'password': 'u5qoleim',
    'server': 'ICMarketsEU-Demo'
}

# account details
login = 51135134
password = 'u5qoleim'
server = 'ICMarketsEU-Demo'

# MongoDB info
cluster = MongoClient("mongodb://localhost:27017")
db = cluster["meta_5_database"]
collection_1 = db["account_meta_1_info"]
collection_2 = db["account_meta_2_info"]
collection_3 = db["account_meta_3_info"]

# connect to MetaTrader 5


def login_auth(login, password, server):
    if not mt5.login(login, password, server):
        print('Not authorized.')
        mt5.shutdown()
    else:
        account_info = mt5.account_info()
        print(account_info)
        account = {}
        for name in range(len(account_info)):
            account['login'] = account_info.login
            account["name"] = account_info.name
            account["balance"] = account_info.balance
            account["equity"] = account_info.equity
            account["server"] = account_info.server
            account["company"] = account_info.company
        print(account)

        # connects to mongodb and adds the account
        collection_3.insert_one(account)

        # get the market watch symbols
        symbols_total = mt5.symbols_get()
        for i in range(len(symbols_total)):
            name = symbols_total[i]._asdict()

            # connects to mongodb and add to the account
            collection_3.insert_one(name)
            print(name)

        history = mt5.history_deals_total(datetime(2022, 1, 1), datetime(2023, 2, 28))

        print(f'History >> {history}')
        mt5.shutdown()


def plot_graph():

    # read the mongodb for an account
    meta_info = pd.read_csv("account_meta_1_info.csv")
    meta_info.info()

    msk = meta_info['login'].values[0]  # login value
    msk_b = meta_info['balance'].values[0]  # balance value
    msk_e = meta_info['equity'].values[0]  # equity value

    pio.renderers.default = 'browser'

    fig = go.Figure(data=[go.Bar(y=[msk_b, msk_e], x=[datetime.now()])], layout_title_text=f'User Account: {msk}\n'
                                                                                  f'Balance: {msk_b}\n'
                                                                                  f'Equity: {msk_e}')
    fig.update_layout(
        updatemenus=[]
    )

    # display dashboard of account user 1
    fig.show()


if __name__ == '__main__':
    print('Initializing......')
    if not mt5.initialize():
        print('Initialize failed.')
        mt5.shutdown()
    else:
        print('Logging in for an account......')
        login_auth(login, password, server)
        plot_graph()
