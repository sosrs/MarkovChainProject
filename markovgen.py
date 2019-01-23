#defining the set of all punctuation this supports. Any non-alphanumeric symbols not included here will be dropped.
punct={'.', '?', '!','...',',',';'}
#defining the set of all punctuation that ends a sentence.
endpunct={'.', '?', '!','...'}

class MarkovDict:
    
    def __init__(self,inputString:str)->None:
        import re
        #defining the set of all punctuation this supports. Any non-alphanumeric symbols not included here will be dropped.
        self.punct={'.', '?', '!','...',',',';'}
        #defining the set of all punctuation that ends a sentence. Words that follow these could be used to begin the passage
        self.endpunct={'.', '?', '!','...'}

        #RegEx to split a string into a list of words
        #current pattern: Any chain of alphanumerics and underscores, or ['$#%&-]
        #note: this will not currently handle quotations or parentheses
        wordList= re.findall(r"[\w'$#%&-]+|[.]{3}|[.,!?;]",inputString)
        
        #The structure is a dictionary with {wordA: {wordB:# of times wordB has followed A}}
        #wordDict['start of passage'] is used to store words that begin a statement, to be able to begin the passage
        #wordDict[wordA]['total points'] is used to store the number of data points we have for words following wordA
        self.wordDict= {
            'start of passage':{
                'total points':1,
                wordList[0]:1}
            }

        while len(wordList)>1:
            currentWord=wordList.pop(0)
            nextWord=wordList[0]
            if currentWord not in self.wordDict:
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
                self.wordDict[currentWord]['total points']+=1
            if currentWord in self.endpunct:
                #if the current word is an ending puctuation, add the next word to dict of words that can begin the passage
                if nextWord not in self.wordDict['start of passage']:
                    self.wordDict['start of passage'][nextWord]=1
                    self.wordDict['start of passage']['total points']+=1
                else:
                    self.wordDict['start of passage'][nextWord]+=1
                    self.wordDict['start of passage']['total points']+=1


    def add_words(self,currentWord:str,nextWord:str)->None:
        #Adds one data point to the dictionary at a time (one word:nextWord pair)
        #if currentWord ='start of passage', it will add the nextWord to possible beginning words
        if currentWord not in self.wordDict:
            self.wordDict[currentWord]={nextWord:1,
                                        'total points':1}
        elif nextWord not in self.wordDict[currentWord]:
            self.wordDict[currentWord][nextWord]=1
            self.wordDict[currentWord]['total points']+=1
        else:
            self.wordDict[currentWord][nextWord]+=1
            self.wordDict[currentWord]['total points']+=1
            

    def get_the_next_word(self, firstWord:str='start of passage')->str:
        import random
        #should put a check here for is your total data points the same as the sum of your data points
        
        #pick a random integer between 0 and the total amount of data points we have for firstWord
        randInt=random.randint(0,self.wordDict[firstWord]['total points']-1)
        counter=0
        
        for key in sorted(self.wordDict[firstWord]):
            counter = counter + self.wordDict[firstWord][key]
            if (key != 'total points') and (randInt < counter):
                return key
        
        #if you made it this far, that means that your random int was greater than the sum of your data points
        #That shouldn't be possible
        print("your rand int for ", firstWord, " is too big!")
                
        
    def generate(self, numOfSentences:int)->str:
        import random
        #currently, the random generator assigns equal probability to each
        #option in the markov chain.
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
            
