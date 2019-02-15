#defining the set of all punctuation this supports. Any non-alphanumeric symbols not included here will be dropped.
punct={'.', '?', '!','...',',',';'}
#defining the set of all punctuation that ends a sentence.
endpunct={'.', '?', '!','...'}

class MarkovDict:
    
    def __init__(self,inputString:str)->None:
        # defining the set of all punctuation this supports. Any non-alphanumeric symbols not included here will be dropped.
        self.punct={'.', '?', '!','...',',',';'}
        # defining the set of all punctuation that ends a sentence. Words that follow these could be used to begin the passage
        self.endpunct={'.', '?', '!','...'}
        
        wordList= self.string_to_list(inputString)
        
        # change this to account for empty strings. this would probably allow us to just use the add_string function
        # instead of replicating it here just to be able to initialize the dictionary
        
        # The structure is a dictionary with {wordA: {wordB:# of times wordB has followed A}}
        # wordDict['start of passage'] is used to store words that begin a statement, to be able to begin the passage
        # wordDict[wordA]['total points'] is used to store the number of data points we have for words following wordA
        self.wordDict= {
            'start of passage':{
                'total points':1,
                wordList[0]:1}
            }

        while len(wordList)>1:
            currentWord=wordList.pop(0)
            nextWord=wordList[0]
            
            self.add_words(currentWord,nextWord)
            
            '''if currentWord not in self.wordDict:
                #if the word is totally new, create the dict for words that can follow it
                self.wordDict[currentWord]={nextWord:1,
                                            'total points':1
                                            }
            elif nextWord not in self.wordDict[currentWord]:
                #if the next word has never followed current word, add an entry for the next word in the following word dict
                #increment the number of data points for current word
                self.wordDict[currentWord][nextWord]=1
                self.wordDict[currentWord]['total points']+=1
            else:
                #increment points for next word following current word, and total points
                self.wordDict[currentWord][nextWord]+=1
                self.wordDict[currentWord]['total points']+=1'''
            if currentWord in self.endpunct:
                #if the current word is an ending puctuation, add the next word to dict of words that can begin the passage
                self.add_words('start of passage',nextWord)
                
                '''nextWord not in self.wordDict['start of passage']:
                    self.wordDict['start of passage'][nextWord]=1
                    self.wordDict['start of passage']['total points']+=1
                else:
                    self.wordDict['start of passage'][nextWord]+=1
                    self.wordDict['start of passage']['total points']+=1'''

    def dictionary(self, word='first level')->dict:
        
        # Method to access the dictionary of data in this MarkovDict
        # this is an abstraction layer to protect precious data
        # I should probably learn if private and public variables are a thing
        
        #todo: implement ability to access the second level dictionary given the first key
        if word=='first level':
            return self.wordDict
        elif word in self.wordDict:
            return self.wordDict[word]
        else:
            print(word+' is not in the first level of this Markov Dictionary')
        
    def string_to_list(self,inputString:str)->list:
        import re
        # RegEx to split a string into a list of allowed words
        # current pattern: Any chain of alphanumerics and underscores, or ['$#%&-]
        # note: this will not currently handle quotations or parentheses
        return re.findall(r"[\w'$#%&-]+|[.]{3}|[.,!?;]",inputString)
        
    def add_words(self,currentWord:str,nextWord:str)->None:
        
        #Adds one data point to the MarkovDict at a time (one word:nextWord pair)
        
        #if currentWord ='start of passage', it will add the nextWord to possible beginning words
        if currentWord not in self.wordDict:
            #if the word is totally new, create the dict for words that can follow it
            self.wordDict[currentWord]={nextWord:1,
                                        'total points':1}
        elif nextWord not in self.wordDict[currentWord]:
            #if the next word has never followed current word, add an entry for the next word in the following word dict
            #increment the number of data points for current word
            self.wordDict[currentWord][nextWord]=1
            self.wordDict[currentWord]['total points']+=1
        else:
            #increment points for next word following current word, and total points
            self.wordDict[currentWord][nextWord]+=1
            self.wordDict[currentWord]['total points']+=1
            
    
    def add_file(self,filename:str)->None:
        thefile = open(filename,'r')

    def add_string(self, inputString:str)->None:
        
        #Adds an entire passage at a time to this MarkovDict
        
        wordList= self.string_to_list(inputString)
        
        while len(wordList)>1:
            currentWord=wordList.pop(0)
            nextWord=wordList[0]
            
            self.add_words(currentWord,nextWord)
            
            if currentWord in self.endpunct:
                #if the current word is an ending puctuation, add the next word to dict of words that can begin the passage
                self.add_words('start of passage',nextWord)
        
    def add_dict(self,child:MarkovDict)->None:
        
        #this will take another MarkovDict as an input, and add its data to this one
        #this will not change the input dict, but will change the current dict
        
        for firstkey in child.dictionary():
            for secondkey in child.dictionary()[firstkey]:
                for tally in range(child.dictionary()[firstkey][secondkey]):
                    self.add_words(firstkey,secondkey)
    
    
    def get_the_next_word(self, firstWord:str='start of passage')->str:
        
        #Given a seed word string, randomly generates a second word string from the list of words that followed it in the seed data.
        #If no seed word is given, the function assumed you are trying to find a word to start a passage.
        
        import random
        #should put a check here for is your total data points the same as the sum of your data points
        
        #pick a random integer between 0 and the total amount of data points we have for firstWord
        randInt=random.randint(0,self.wordDict[firstWord]['total points']-1)
        counter=0
        
        for key in sorted(self.wordDict[firstWord]):
            #For each wordB, add the number of times that word has followed, then check if the running total is greater than
            #the random integer. If so, return that word. This creates a weighted probability.
            counter = counter + self.wordDict[firstWord][key]
            if (key != 'total points') and (randInt < counter):
                return key
        
        #if you made it this far, that means that your random int was greater than the sum of your data points
        #That shouldn't be possible. Exception to be coded here.
        print("your rand int for ", firstWord, " is too big!")
                
        
    def generate(self, numOfSentences:int)->str:
        
        #Given an integer, generates that many sentences of predicted text from the stored word dictionary
        #If the generated passage ends with a word or symbol that only ended passages from the seed text,
        #the generator will not be able to continue and will display what it had. This behaviour should go away
        #with enough seed data.
        
        import random

        output=[self.get_the_next_word()]

        lastWord=output[0]
        sentenceCount=0

        while sentenceCount<numOfSentences:
            #if somehow we are directed to a word that does not have a next word, end the chain there
            if lastWord not in self.wordDict:
                print("I could only make %i complete sentences:" % sentenceCount)
                return ''.join(output)
            
            lastWord=self.get_the_next_word(lastWord)
            if lastWord in self.endpunct:
                sentenceCount+=1
            elif lastWord not in self.punct:
                output.append(' ')
            output.append(lastWord)
        
        return ''.join(output)
            
#these functions were the proof of concept, and are now obsolete with the creation of the MarkovDict class
def markov_input(literature:str)->dict:
    '''import re

    #RegEx to split a string into a list of words
    #current pattern: Any chain of alphanumerics and underscores, or ['$#%&-]
    #note: this will not currently handle quotations or parentheses
    wordList= re.findall(r"[\w'$#%&-]+|[.]{3}|[.,!?;]",literature)
    
    
    #Initialize the dict of words with a set for what could start a sentence.
    wordDict= {'start of passage':{wordList[0],}}

    while len(wordList)>1:
        current=wordList.pop(0)        
        if current not in wordDict:
            wordDict[current]={wordList[0],}
        else:
            wordDict[current].add(wordList[0])
        if current in endpunct:
            wordDict['start of passage'].add(wordList[0])'''
    return MarkovDict(literature)

def markov_output(wordDict:dict, numOfSentences:int)->str:
    import random

    #currently, the random generator assigns equal probability to each
    #option in the markov chain.
    output=random.sample(wordDict['start of passage'],1)
    
    lastWord=output[0]
    sentenceCount=0
    
    while sentenceCount<numOfSentences:
        lastWord=random.sample(wordDict[lastWord],1)[0]
        if lastWord in endpunct:
            sentenceCount+=1
        elif lastWord not in punct:
            output.append(' ')
        output.append(lastWord)
        
        #if somehow we are directed to a word that does not have a next word, end the chain there
        if lastWord not in wordDict:
            print("I could only make %i complete sentences:" % sentenceCount)
            return ''.join(output)
        
    return ''.join(output)
            
