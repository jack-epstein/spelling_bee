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
st.write("The rules of Spelling Bee are simple: you are given 7 letters to make words. One of these letters must be included in every word and all words must only consist of this letter plus some of the other 6. Words must be four letters or longer. Each day, there are 1+ pangram(s), which include all 7 letters.") 

st.write("It is worth noting that this is NOT the same source of words the New York Times uses, so the lists this script may output certain words that are not accepted by the game, and could potentially miss some used by the NY Times. I am unable to find the list that they use. If you see a word that the game won't accept or a word missing from this list, please let me know!")
    
st.write("To play the game, go to this link: https://www.nytimes.com/puzzles/spelling-bee. Obviously, I would consider using this app as a form of cheating (but I won't tell.)")


#read in words 
df = pd.read_csv('data/words.csv')

df['word_length'] = df.word.str.len() #get column of word length
df = df.loc[df.word_length >= 4] #filter out words shorter than 4 letters

# save list of words not in new york times list -- can be updated
not_in_list = ['continuo','cony','coon','iconicity','initio','nicotinic','nuncio','toto','yoyo','eigne','geeing',
              'ginnie','whig','algid','diallage','gael','gail','gaza','geed','gelid','lege','allah','althea','athena',
              'ethel','halloo','hanna','hannah','helen','helena','leah','loth','nathan','noah','othello']
df = df.loc[~df.word.isin(not_in_list)].copy() #filter these out

# save list of words missing from our dataset -- can be updated
missing = ['naan','cocci','cutout','oniony','toon','gigging','agaze','algal','deglaze','deglazed','eagled','geez','gelee',
          'gigged','glia','zagged','zigged']
df = pd.concat((df, pd.DataFrame(missing,columns=['word'])))


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

    
    
