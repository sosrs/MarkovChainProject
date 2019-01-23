punct={'.', '?', '!','...',',',';'}
endpunct={'.', '?', '!','...'}
class MarkovDict:
    def __init__(self,inputString:str)->None:
        import re
        wordList= re.findall(r"[\w'$#%&-]+|[.]{3}|[.,!?;]",inputString)
        self.wordDict= {'start of passage':{wordList[0],}}
        while len(wordList)>1:
            current=wordList.pop(0)        
            if current not in wordDict:
                self.wordDict[current]={wordList[0],}
            else:
                self.wordDict[current].add(wordList[0])
            if current in endpunct:
                self.wordDict['start of passage'].add(wordList[0])
            

def markov_input(literature:str)->dict:
    import re

    #RegEx to split a string into a list of words
    #current pattern: Any chain of alphanumerics and underscores, or ['$#%&-]
    #note: this will not currently handle quotations or parentheses
    wordList= re.findall(r"[\w'$#%&-]+|[.]{3}|[.,!?;]",literature)
    
    #print(wordList)
    
    #Initialize the dict of words with a set for what could start a sentence.
    wordDict= {'start of passage':{wordList[0],}}

    while len(wordList)>1:
        current=wordList.pop(0)        
        if current not in wordDict:
            wordDict[current]={wordList[0],}
        else:
            wordDict[current].add(wordList[0])
        if current in endpunct:
            wordDict['start of passage'].add(wordList[0])
    return wordDict

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
        
    return ''.join(output)
            
