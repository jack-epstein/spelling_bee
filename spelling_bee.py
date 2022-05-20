#clean these up
import os
import sys
import numpy as np
import pandas as pd


#read in words -- find better source
df = pd.read_csv('https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt',names=['word'])


df['word_length'] = df.word.str.len() #get column of word length
df = df.loc[df.word_length >= 4] #filter out words shorter than 4 letters

#MAKE THIS DYNAMIC FOR LETTERS
middle_letter = 'r'
all_letters = ['r','u','y','h','n','a','c']
df = df.loc[df.word.str.contains(middle_letter)] #all words need middle letter


for i in range(6):
    df[i] = df.word.str.contains(other_letters[i])
    
df['all'] = df[0] & df[1] & df[2] & df[3] & df[4] & df[5]


def letter_check(word):
    check_list = [l in all_letters for l in word]
    
    return all(check_list)


df['check'] = df.apply(lambda x: letter_check(x['word']), axis=1)

df = df.loc[df['check']].copy()


for i in df.loc[df['check'] & df['all']]['word']:
    print(i)
    
    
for i in df.loc[df['check']]['word']:
    print(i)
