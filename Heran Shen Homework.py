def send_message(state, message):
    global Stock
#     print("USER : {}".format(message))
    print(user_template.format(message))
    new_state, response = respond(state, message)
#     print("BOT : {}".format(response))
    print(bot_template.format(response))
    if response == "Ok, here's what you want: ":
        search(Stock, stock, entity, date)
        print(bot_template.format("Do you want to take a look at its historical price?"))
    if response == "Here's the historical abstract price chart":
        get_monthly_abstract_price(stock)
        print(bot_template.format("Do you need anything else?"))
    return new_state

def respond(state, message):
    (new_state, response) = policy_rule[(state, interpret(message, state))]
    return new_state, response

def interpret(message,state):
    ##### three entities are global variables
    global stock, entity, date
    ##################### state == INIT #####################
    if state == INIT:
        msg = message.lower()
        intent = interpreter.parse(msg)["intent"]['name']
        if intent == "ask_for_help" or intent == 'greet' or intent == 'affirm':
            return 'activate'
        ## Asking contextual questions
        if 'what' in msg:
            return 'ask_explanation'
    ################## state == CHOOSE_STOCK ##################
    elif state == CHOOSE_STOCK:
        pattern_stock = re.compile('([A-Z]{2,})')
        searchObj = re.search(pattern_stock, message)
        if searchObj:
            stock = searchObj.group()
            doc = nlp(message)
            for token in doc:
                if token.text == stock:
                    ent = list(a for a in list(token.ancestors) if a.pos_ == 'NOUN')
            if len(ent) == 0 or str(ent[-1]) not in ['price','Price', 'volume','Volume', 'cashflow','Cashflow', 'cash flow', 'Cash flow', 'Cash Flow']:
                return('specify_stock_without_entity')
            else:
                entity = ent[0]
                return('specify_stock_with_entity')
        else:
            return('none')
        
    ################## state == CHOOSE_ENTITY ##################
    elif state == CHOOSE_ENTITY:
        for ent in ['price', 'volume', 'cashflow', 'cash flow']:
            if ent in message:
                entity = ent
                return 'specify_stock_with_entity'
        return 'none'
    
    ################## state == CHOOSE_DATE ##################
    elif state == CHOOSE_DATE:
        pattern_date = re.compile('(0*[1-9]|1[0-2])[-|\.|\/](3[0-1]|2[0-9]|1[0-9]|0*[1-9])')
        searchObj = re.search(pattern_date, message)
        if searchObj:
            date.extend([int(searchObj.group(1)), int(searchObj.group(2))])
            return 'specify_date'
        else:
            return 'none'
        
    ################## state == CHOOSE_DATE ##################
    elif state == HISTORICAL:
        msg = message.lower()
        intent = interpreter.parse(msg)["intent"]['name']
        if intent == 'negate':
            return 'none'
        else:
            return 'yes'
    
    ################## state == ASK_OTHER ###################   
    elif state == ASK_OTHER:
        msg = message.lower()
        intent = interpreter.parse(msg)["intent"]['name']
        if intent == 'negate':
            return 'none'
        else:
            pattern_stock = re.compile('([A-Z]{2,})')
            searchObj = re.search(pattern_stock, message)
            if searchObj:
                stock = searchObj.group()
                doc = nlp(message)
                for token in doc:
                    if token.text == stock:
                        ent = list(a for a in list(token.ancestors) if a.pos_ == 'NOUN')
                if len(ent) == 0 or str(ent[-1]) not in ['price','Price', 'volume','Volume', 'cashflow','Cashflow', 'cash flow', 'Cash flow', 'Cash Flow']:
                    return('specify_stock_without_entity')
                else:
                    entity = ent[0]
                    return('specify_stock_with_entity')
            else:
                return('yes')
            
    return 'none'

def send_messages(messages):
    state = INIT
    for msg in messages:
        state = send_message(state, msg)

def search(Stock, stock, entity, date):
    goal = Stock(stock, token=Token)
    if str(entity) == 'cashflow':
        print("The {} of {} is {}".format(str(entity), stock, goal.get_cash_flow()['cashflow'][0]['cashFlow']))
    elif str(entity) == 'volume':
        print("The {} of {} is {}".format(str(entity), stock, str(goal.get_quote()['avgTotalVolume'])))
    else:
        print("The {} of {} is {}".format(str(entity), stock, str(goal.get_quote()['latestPrice'])))

def _plot_day_summary(ax, quotes, ticksize=3,
                      colorup='k', colordown='r',
                      ochl=True):
    """Plots day summary
        Represent the time, open, high, low, close as a vertical line
        ranging from low to high.  The left tick is the open and the right
        tick is the close.
    Parameters
    ----------
    ax : `Axes`
        an `Axes` instance to plot to
    quotes : sequence of quote sequences
        data to plot.  time must be in float date format - see date2num
        (time, open, high, low, close, ...) vs
        (time, open, close, high, low, ...)
        set by `ochl`
    ticksize : int
        open/close tick marker in points
    colorup : color
        the color of the lines where close >= open
    colordown : color
        the color of the lines where close <  open
    ochl: bool
        argument to select between ochl and ohlc ordering of quotes
    Returns
    -------
    lines : list
        list of tuples of the lines added (one tuple per quote)
    """
    # unfortunately this has a different return type than plot_day_summary2_*
    lines = []
    for q in quotes:
        if ochl:
            t, ope, close, high, low = q[:5]
        else:
            t, ope, high, low, close = q[:5]

        if close >= ope:
            color = colorup
        else:
            color = colordown

        vline = Line2D(xdata=(t, t), ydata=(low, high),
                       color=color,
                       antialiased=False,   # no need to antialias vert lines
                       )

        oline = Line2D(xdata=(t, t), ydata=(ope, ope),
                       color=color,
                       antialiased=False,
                       marker=TICKLEFT,
                       markersize=ticksize,
                       )

        cline = Line2D(xdata=(t, t), ydata=(close, close),
                       color=color,
                       antialiased=False,
                       markersize=ticksize,
                       marker=TICKRIGHT)

        lines.extend((vline, oline, cline))
        ax.add_line(vline)
        ax.add_line(oline)
        ax.add_line(cline)

    ax.autoscale_view()

    return lines

def plot_day_summary_oclh(ax, quotes, ticksize=3,
                          colorup='k', colordown='r'):
    return _plot_day_summary(ax, quotes, ticksize=ticksize,
                             colorup=colorup, colordown=colordown,
                             ochl=True)

def get_monthly_abstract_price(company):
    print("Company: ", company)   
    # get data from iexfinance 
    goal = Stock(company, token=Token)
    mon_pri_dics = goal.get_historical_prices() 
    # create a new list
    mon_pri_data = []
    # change the data into the form that mpf.candlestick_ochl function can read
    for dic in mon_pri_dics:
        # get date open high low close volume
        list(dic.values())[0:6]
        # change date into number
        t = date2num(datetime.datetime.strptime(list(dic.values())[0], '%Y-%m-%d'))
        # change sequence into the form that mpf.candlestick_ochl function can read
        ope, close, high, low, vol = list(dic.values())[1:6]
#         print(ope, close, high, low, vol)
         # change the data into the form that mpf.candlestick_ochl function can read
        data = [t, ope, close, high, low, vol]
        mon_pri_data.append(data)
    
    # draw the figure
    # set ax as the style of figure   
    fig, ax = plt.subplots(figsize = (15,3.5))
    plt.rcParams['savefig.dpi'] = 500
    # set parameters of plot_day_summary_oclh: ax = ax sample; mon_pri_data = data color up = close > open; color down = open > close
    
    plot_day_summary_oclh(ax, mon_pri_data, colorup = 'r', colordown = 'g')
    ax.set_title('Candlestick Abstract Chart of' + ' ' + company)
    plt.grid(True)
    # set price label
    plt.ylabel('Price')
    # set x axis as date
    ax.xaxis_date ()
    plt.show()
    return plt.savefig('monthabstractprice.png')

bot_template = "BOT : {0}"
user_template = "USER : {0}"
Token = "pk_5f52eaa0a4d14a30983d085b30b580e7"

# Import necessary modules
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config

from iexfinance.stocks import Stock

import re
import spacy

# Import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.pylab import date2num
from matplotlib.lines import TICKLEFT, TICKRIGHT, Line2D

# Import datetime
import datetime

nlp = spacy.load("en_core_web_md")

# Create a trainer that uses this config
trainer = Trainer(config.load("config_spacy.yml"))

# Load the training data
training_data = load_data('stock_training.json')

# Create an interpreter by training the model
interpreter = trainer.train(training_data)

# Define the states
INIT = 0
CHOOSE_STOCK = 1
CHOOSE_DATE = 2
CHOOSE_ENTITY = 3
HISTORICAL = 4
ASK_OTHER = 5
FINISH = 6

state = INIT
stock = None # store name of the stock
entity = None #store entity to find
date = [] # store the required date
# Define policy rules
policy_rule = {
    (INIT, "activate"): (CHOOSE_STOCK, "What can I do for you?"),
    (INIT, "none"): (INIT, "I'm sorry - I'm not sure how to help you"),
    (INIT, "ask_explanation"): (INIT, "I'm a bot to offer price, volume or cashflow of stocks"),
    
    (CHOOSE_STOCK, "specify_stock_with_entity"): (CHOOSE_DATE, "Well, which date are you interested in?"),
    (CHOOSE_STOCK, "specify_stock_without_entity"): (CHOOSE_ENTITY, "What information do you need?"),
    (CHOOSE_STOCK, "none"): (CHOOSE_STOCK, "I'm sorry - I can't identify this stock."),
    
    (CHOOSE_ENTITY, "specify_stock_with_entity"): (CHOOSE_DATE, "Perfect, which date are you interested in?"),
    (CHOOSE_ENTITY, "none"): (CHOOSE_ENTITY, "I'm sorry - I can only search price, volume, and cashflow."),
    
    (CHOOSE_DATE, "specify_date"): (HISTORICAL, "Ok, here's what you want: "),
    (CHOOSE_DATE, "none"): (CHOOSE_DATE, "I'm sorry - I need a specific day"),
    
    (HISTORICAL, "yes"): (ASK_OTHER, "Here's the historical abstract price chart"),
    (HISTORICAL, "none"): (ASK_OTHER, "Ok, do you need anything else?"),
    
    (ASK_OTHER, "none"): (FINISH, "Good bye, see you next time"),
    (ASK_OTHER, "specify_stock_with_entity"): (CHOOSE_DATE, "Well, which date are you interested in?"),
    (ASK_OTHER, "specify_stock_without_entity"): (CHOOSE_ENTITY, "What information do you need?"),
    (ASK_OTHER, "yes"): (CHOOSE_STOCK, "Ok, which stock do you want?")
    
}

send_messages([
    "can you help me",
    "what's the price of AAPL",   
    "5-29",
    "Yes",
    "Yes",
    "TSLA's volume",
    "7.2",    
    "No",
    "No"
])
