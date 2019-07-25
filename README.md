# Chatbot
A chatbot used for searching the required real-time information of a stock is presented. Its framework is based on `Rasa_NLU` with `"spacy_sklearn"` as its foundation. Pre-defined sentences and phrases are trained to identify `intents` from natural language related to stock information inquiry. By implementing `slot filling`, `finite state machine` and `regular expression`, users can acquire the desired information about the given stock by employing dialogues.


First, the user need to activate the chatbot by greeting or asking for help.

Second, the user can input the company's name he want. The robot will detect whether a specifc goal is given, like the price, volume or cashflow of the stock.

Third, if the goal is already given, then this step will be skipped, otherwise, the chatbot will ask the user to input a valid one.

Then, a valid date in specific structure needs be input.

Finally, after gaining all necessary information, the result will be output.
