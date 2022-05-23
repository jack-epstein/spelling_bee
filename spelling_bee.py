#read in packages
import numpy as np
import pandas as pd



#1. READ IN WORDS WITH INITIAL CLEANING

#read in words -- could potentially improve source
df = pd.read_csv('https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt',names=['word'])

df['word_length'] = df.word.str.len() #get column of word length
df = df.loc[df.word_length >= 4] #filter out words shorter than 4 letters



#2. INPUT LETTERS FOR DAY'S SPELLING BEE

all_letters = [] #initiate an empty list to hold letters
middle_letter = input("Enter Middle Letter: ") #user inputs middle letter
all_letters.append(middle_letter) #append middle letter to the list of all letters

others = input("Enter other letters separated by space: ") #user inputs other letters
others = others.split() #split these into a list
#add each letter to our list of all letters
for o in others:
    all_letters.append(o)
    
    

# 3. NARROW DOWN WORD LIST

df = df.loc[df.word.str.contains(middle_letter)] #all words need middle letter

#make a column for words containing every letter
for i in range(6):
    df[i] = df.word.str.contains(others[i])    
df['all'] = df[0] & df[1] & df[2] & df[3] & df[4] & df[5]


#create a function that takes in a string and checks if every character in that string is in our letter list
def letter_check(word):
    check_list = [l in all_letters for l in word] #creates a list of string length with T/F indicator if letter is in list
    return all(check_list) #returns true only if all true

#apply this function to our list and then shrink dataframe to only have allowed words
df['check'] = df.apply(lambda x: letter_check(x['word']), axis=1)
df = df.loc[df['check']].copy()



# 4. RESULTS

#print pangrams  
print('')
print("Today's Pangram(s):")
for w in df.loc[df['all']]['word']:
    print(w)
print('')
print('')
    
#print all words
print("Today's Words (total={})".format(df.shape[0]))
print(list(df['word']))

