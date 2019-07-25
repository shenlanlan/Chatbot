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


## Requirements
### Rasa NLU `pip install rasa_nlu `
[Rasa NLU](https://www.rasa.com/) is a framework of natural language processing, it is applied to train the pre-built dataset.

### iexfinance `pip3 install iexfinance`
[iexfinance](https://pypi.org/project/iexfinance/0.3.1/) is a practical api system to obtain various data of stocks:<br>


### Matplotlib `pip install -U matplotlib`


## Usage Guide
   
## Contact
Heran Shen, hs3045@columbia.edu

## Acknowledge
This project is supervised by Ph.D Fan Zhang](http://www.mit.edu/~f_zhang/) at IBM & MIT. Great thanks to his advice and help.








First, the user need to activate the chatbot by greeting or asking for help.

Second, the user can input the company's name he want. The robot will detect whether a specifc goal is given, like the price, volume or cashflow of the stock.

Third, if the goal is already given, then this step will be skipped, otherwise, the chatbot will ask the user to input a valid one.

Then, a valid date in specific structure needs be input.

Finally, after gaining all necessary information, the result will be output.
