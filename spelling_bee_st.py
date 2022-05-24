import pandas as pd
import numpy as np
import streamlit as st
import string


#create a function that takes in a string and checks if every character in that string is in our letter list
def letter_check(word):
    check_list = [l in all_letters for l in word] #creates a list of string length with T/F indicator if letter is in list
    return all(check_list) #returns true only if all true
    
    

#1. READ IN WORDS WITH INITIAL CLEANING
st.title('NYT Spelling Bee App')

#read in words 
df = pd.read_csv('data/usa2.txt',names=['word'])

df['word_length'] = df.word.str.len() #get column of word length
df = df.loc[df.word_length >= 4] #filter out words shorter than 4 letters



#2. INPUT LETTERS FOR DAY'S SPELLING BEE 
st.header('Letter Selection')

alphabet_string = string.ascii_lowercase
alphabet_list = list(alphabet_string)

all_letters = [] #initiate an empty list to hold letters
middle_letter = st.selectbox("Choose Middle Letter",alphabet_list) #user inputs middle letter
all_letters.append(middle_letter) #append middle letter to the list of all letters


others = st.multiselect("Choose All Other Letters",alphabet_list) #user inputs other letters

#add each letter to our list of all letters
for o in others:
    all_letters.append(o)
    


if len(others) != 6:
    st.write('Please Choose 6 Additional Letters', color='red')
    
else:    

    # 3. NARROW DOWN WORD LIST
    df = df.loc[df.word.str.contains(middle_letter)] #all words need middle letter

    #make a column for words containing every letter
    for i in range(6):
        df[i] = df.word.str.contains(others[i])    
    df['all'] = df[0] & df[1] & df[2] & df[3] & df[4] & df[5]


    #apply this function to our list and then shrink dataframe to only have allowed words
    df['check'] = df.apply(lambda x: letter_check(x['word']), axis=1)
    df = df.loc[df['check']].copy()



    # 4. RESULTS
    st.header("Today's Pangram(s):")
    for w in df.loc[df['all']]['word']:
        st.subheader(w)

    n_words = df.shape[0]  
    n_words_4 = np.ceil(n_words/4).astype(int)

    st.header("Full List of Words (total={}):".format(n_words))
    words = list(df['word'])


    col1, col2, col3, col4 = st.columns(4)

    with col1:
        for i in words[0:n_words_4]:
            st.write(i)

    with col2:
        for i in words[n_words_4:2*n_words_4]:
            st.write(i)

    with col3:
        for i in words[2*n_words_4:3*n_words_4]:
            st.write(i)

    with col4:
        for i in words[3*n_words_4:]:
            st.write(i)

    
    