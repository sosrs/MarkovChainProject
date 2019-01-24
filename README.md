# MarkovChainProject
Module to create a markov chain text generator using an input string of data

V 0.2
Created function to take in a string of data and generate a dictionary of words to be used in a Markov chain generator

Created function to take in a dictionary of words:following words to generate text.

V 0.3
Expanded the data structure to support weighted probabilities based on how many times a word is followed by a second

Created the MarkovDict class to support this data structure

Created constructor and text generator methods from old functions

V 0.35
No additional functionality, but began abstraction layer to access the MarkovDict's dictionaries

Also created a function for converting a string to list of allowed words, adding a whole passage to the MarkovDict

Began removing redundant code with creation of above functions

Began function to add an existing MarkovDict to the current MarkovDict (only alters current)

TODO:
Finish function to be able to combine said dictionaries to easily pull data from several passages

Finish abstraction method to access dictionaries

Add ability to create a MarkovDict from a text file, not just a string
