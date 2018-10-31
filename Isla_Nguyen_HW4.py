# Aileen Isla & Ngoc Nguyen
# CS141 Lab Wed. 2pm
# HW4
# This program calculates the sentiments in real twitter data
# from Feb. 19 and Feb 25 for a given word. Then creates a map
# that displays the mood in each state for the word.


import codecs
import json
from simplemapplot import make_us_state_map

stateAbbrevList = ["AK","AL","AR","AZ","CA","CO","CT","DE",
                   "FL","GA","HI","IA","ID", "IL","IN","KS",
                   "KY","LA","MA","MD","ME","MI","MN","MO",
                   "MS","MT","NC","ND","NE","NH","NJ","NM",
                   "NV","NY", "OH","OK","OR","PA","RI","SC",
                   "SD","TN","TX","UT","VA", "VT", "WA","WI",
                   "WV","WY"]

SENTIMENTCOLORS = ["#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#bababa", "#fee090", "#fdae61", "#f46d43", "#d73027"]

def parseTweet(line):
    ''' str -> list
    PRE:  takes a string that is one tweet with metadata
    POST: returns a list extracting several fields from the tweet
          ordered as: [0] date, [1] id, [2] text of tweet,
          [3] number of followers,[4] number of friends, [5] country,
          [6] city, state.  Note the last field is a single string
          with the city name followed by a comma by the state abbrev.
    '''
    tweet = json.loads(line)
    date = tweet['created_at']
    id = tweet['id']
    numFollowers = tweet['user']['followers_count']
    numFriends = tweet['user']['friends_count']
    country = tweet['place']['country_code']
    cityState = tweet['place']['full_name']

    if 'retweeted_status' in tweet:
    	text = tweet['retweeted_status']['text']
    else:
    	text = tweet['text']
    	
    return [date, id, text, numFollowers, numFriends, country, cityState]


def readTweetFile(tList, filename):
    '''list, str -> void
    This function takes in a list and the filename of a json file of tweets.
    It reads the json file line by line and extracts some fields from that
    file and puts combines those fields into a list and appends the list to tList.  
    '''

    tweetFile = codecs.open(filename, 'r', 'utf-8')
    for line in tweetFile:
        try:
            item = parseTweet(line)
            if item[5] == "US" and item[6][-2:] in stateAbbrevList:
                tList.append(item)
                #print(tweetList[-1])  #Uncomment this line of code if you want to see the list of valid tweets.
                                       #This can be helpful when you're working with the sandwich.json file but
                                       #definitely not helpful when you're working with the large data files!
        except:
            pass
    tweetFile.close()


##    
#userWord count in every tweet
    
def countDict(userWord, tweetList, stateCountDict):
    """ str, list, dict -> dict
    PRE: Takes in user input, tweetList[2], and the empty
         stateCountDict
    POST: Return stateCountDict(key = state abbreviation, value = int)
    This function looks through each Twitter sentence, when the word is
    in the sentence it adds 1 to the respected state.
    """
    
    for line in tweetList:
        
        if userWord in line[2].lower():
            
            word = line[6][-2:]
            stateCountDict[word] += 1
    
    return stateCountDict


##
#sentiment score for every state

def sentimentScore(sentimentDict, userWord, tweetList, stateSentimentScoreDict):
    """ dict, str, list, dict -> dict
    PRE: Takes in sentimentDict, user input, twitter sentences and empty stateSentimentScoreDict dictionary
    POST: Return updated stateSentimentScoreDict with positive or negative values
    So this function basically read through the twitter sentences that has user input AND
    the key of sentimentDict, then it dictates the value for stateSentimentScoreDict respective to
    each state. 
    """
    
    for line in tweetList:
        if userWord in line[2].lower():
            
            for word in sentimentDict.keys():
                if word in line[2].lower():
                
                    citystate = line[6][-2:]
                    (stateSentimentScoreDict[citystate]) += (sentimentDict[word])
              
    return stateSentimentScoreDict



##
#avg sentiment

def avgSentiment(stateSentimentScoreDict, stateCountDict):
    """ dict, dict -> dict
    PRE: Takes in multiple dictionaries with values
    POST: Return an average of the updated dictionary
    This function calculates the average based on the values from each dictionary
    """
    
    for state in stateSentimentScoreDict.keys():
        
        if state in stateCountDict.keys():

            if stateCountDict[state] == 0:
                stateSentimentScoreDict[state] = 0
                
            if stateCountDict[state] > 0:
                stateSentimentScoreDict[state] = (stateSentimentScoreDict[state]) / (stateCountDict[state])
                
    return stateSentimentScoreDict

    
##
#assigning colors
def assignSentimentColors(stateSentimentScoreDict, SENTIMENTCOLORS):
    """ dict, list -> dict
    PRE: takes in a dictionary and the color list
    POST: return a dict(key = abbreviated state, value = color code(str))
    This functions finds the max and min of the values from stateSentimentScoreDict.
    Then reads through each state to assign a color based on the value's ratio between max/min. 
    """
    
    MAXsentiment = max(stateSentimentScoreDict.keys(), key=(lambda state: stateSentimentScoreDict[state]))
    MINsentiment = min(stateSentimentScoreDict.keys(), key=(lambda state: stateSentimentScoreDict[state]))
    
    x = stateSentimentScoreDict[MINsentiment]
    y = stateSentimentScoreDict[MAXsentiment]
    
    for state in stateSentimentScoreDict.keys():
        
        if stateSentimentScoreDict[state] > 0: 
            
            if stateSentimentScoreDict[state] > (y*.60): #above 60% 
                stateSentimentScoreDict[state] = 8 #SENTIMENTCOLORS[8]
                
            elif stateSentimentScoreDict[state] > (y*.30): #above 30%
                stateSentimentScoreDict[state] = 7 #SENTIMENTCOLORS[7] 
            elif stateSentimentScoreDict[state] > (y*.15): #above 15%
                stateSentimentScoreDict[state] = 6 #SENTIMENTCOLORS[6] 
            elif stateSentimentScoreDict[state] < (y*.15): #below 15%: 
                stateSentimentScoreDict[state] = 5 #SENTIMENTCOLORS[5]
                
        elif stateSentimentScoreDict[state] < 0:
            
            if stateSentimentScoreDict[state] <= (x*.60): #above 60%
                stateSentimentScoreDict[state] = 0 #SENTIMENTCOLORS[0]
            elif stateSentimentScoreDict[state] <= (x*.30): #above 30%
                stateSentimentScoreDict[state] = 1 #SENTIMENTCOLORS[1] 
            elif stateSentimentScoreDict[state] <= (x*.15): #above 15%
                stateSentimentScoreDict[state] = 2 #SENTIMENTCOLORS[2] 
            elif stateSentimentScoreDict[state] > (x*.15): #below 15% 
                stateSentimentScoreDict[state] = 3 #SENTIMENTCOLORS[3]
           
        elif stateSentimentScoreDict[state] == 0:
            stateSentimentScoreDict[state] = 4 #SENTIMENTCOLORS[4]

                
    return stateSentimentScoreDict

    

###################################################################################
# MAIN
#

tweetList = []
sentimentDict = {}
stateCountDict = {}
stateSentimentScoreDict = {}

for state in stateAbbrevList:
    stateCountDict[state] = 0
    stateSentimentScoreDict[state] = 0

#readTweetFile(tweetList,"sandwich.json")
readTweetFile(tweetList,"usaTweetsFeb25.json")
readTweetFile(tweetList,"usaTweetsFeb19.json")


inFile = open('sentimentsFull.csv', 'r')
for line in inFile:
    data = line.split(',')
    sentimentDict[data[0]] = float(data[1])   
inFile.close()

#asks for user Input
userWord = input('Enter a word to search ')
userWord = userWord.lower()


stateCountDict = countDict(userWord, tweetList, stateCountDict)
stateCountDictLIST = list(stateCountDict.items()) 
stateCountDictLIST.sort() #sort the list
print("\nThis is the state's count of user's input sorted by state\n", stateCountDictLIST)

#stateSentimentScoreDict updating from functions
stateSentimentScoreDict = sentimentScore(sentimentDict, userWord, tweetList, stateSentimentScoreDict)
stateSentimentScoreDict = avgSentiment(stateSentimentScoreDict, stateCountDict)
stateSentimentScoreDictLIST = list(stateSentimentScoreDict.items()) 
stateSentimentScoreDictLIST.sort() #sort the list
print("\nThis is the average sentiment score sorted by state\n",stateSentimentScoreDictLIST)

#assign color then create map in directory
stateSentimentScoreDict = assignSentimentColors(stateSentimentScoreDict, SENTIMENTCOLORS)
make_us_state_map(stateSentimentScoreDict, SENTIMENTCOLORS)






