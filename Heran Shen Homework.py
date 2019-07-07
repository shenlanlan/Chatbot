def send_message(state, message):
#     print("USER : {}".format(message))
    print(user_template.format(message))
    new_state, response = respond(state, message)
#     print("BOT : {}".format(response))
    print(bot_template.format(response))
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
FINISH = 4

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
    
    (CHOOSE_DATE, "specify_date"): (FINISH, "Ok, here's what you want: "),
    (CHOOSE_DATE, "none"): (CHOOSE_DATE, "I'm sorry - I need a specific day")
}

send_messages([
    "can you help me",
    "what's the price of AAPL",
    
    "5-29"
])
search(Stock, stock, entity, date)