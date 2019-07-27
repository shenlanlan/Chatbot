# Chatbot
A chatbot used for searching the required real-time information of a stock is presented. Its framework is based on `Rasa_NLU` with `"spacy_sklearn"` as its foundation. Pre-defined sentences and phrases are trained to identify `intents` from natural language related to stock information inquiry. By implementing `slot filling`, `finite state machine` and `regular expression`, users can acquire the desired information about the given stock by employing dialogues.

## Content
* [Function Presentation](#function-presentation)
* [Requirements](#requirements)
   * Rasa NLU
   * iexfinance
   * Matplotlib
* [Usage Guide](#usage-guide)
   * Create NLU dataset and entity dataset
   * Define NLU model configuration
   * Train NLU model
   * Call API of iexfinance & wxpy
   * Try it out
* [Contact](#contact)
* [Acknowledge](#acknowledge)

## Function Presentation
The picture below presents chatbot's basic function.
![Abstract_Chart](https://github.com/shenlanlan/Chatbot/blob/master/Abstract%20Chart.png)

## Requirements
1. Rasa NLU `pip install rasa_nlu `<br>
[Rasa NLU](https://www.rasa.com/) is a framework of natural language processing, it is applied to train the pre-built dataset.

2. iexfinance `pip3 install iexfinance`<br>
[iexfinance](https://pypi.org/project/iexfinance/0.3.1/) is a practical api system to obtain various data of stocks.<br>


3. Matplotlib `pip install -U matplotlib`<br>


## Usage Guide
1. Define Rasa NLU training configuration<br>
Due to the limitation of example amount in the corpus of stock information, "spacy_sklearn" pipeline is implemented to configure the model. By loading the configuration and training the pre-defined dataset, an interpreter can be generated to understand input sentences in the future. Alternative choices are provided at [Rasa NLU](https://rasa.com/docs/nlu/choosing_pipeline/).<br>
The configuration used in the project is shown as follows:<br>
```
language: "en"

pipeline: "spacy_sklearn"

```
In this configuration, `intents` are classified by `a linear SVM`. `Regular expression` is also used in intent classifier to simplify identification.<br> 

2. Create Rasa NLU training dataset<br>
A dataset needs to be trained to identify `intents` and `entities` in user's messages. The dataset (called 'stock_training.json' in this project) is in the form of `JSON`, and several intents and entities in different expressions are defined. For example:
```
{
  "rasa_nlu_data": {
    "common_examples": [
      {
        "text": "hey", 
        "intent": "greet", 
        "entities": []
      }, 
      {
        "text": "can you give me some information of AAPL",
        "intent": "stock_search",
        "entities": [
          {
            "start": 36,
            "end": 40,
            "value": "AAPL",
            "entity": "company"
          }
        ]
      }
    ]
  }
}
```

3. Train Rasa NLU model<br>
With the loaded configuration and dataset, the project can train the model to generate an interpretor, which can identify `intents` and `entities`.
```
# Import necessary modules
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config

nlp = spacy.load("en_core_web_md")

# Create a trainer that uses this config
trainer = Trainer(config.load("config_spacy.yml"))

# Load the training data
training_data = load_data('stock_training.json')

# Create an interpreter by training the model
interpreter = trainer.train(training_data)
```
   
## Contact
Heran Shen, hs3045@columbia.edu

## Acknowledge
This project is supervised by Ph.D Fan Zhang](http://www.mit.edu/~f_zhang/) at IBM & MIT. Great thanks to his advice and help.

