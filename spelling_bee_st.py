import pandas as pd
import numpy as np
import streamlit as st
import string


ADDED_WORD_LIST = [
    'naan', 'cocci', 'cutout', 'oniony', 'toon', 'gigging', 'agaze', 'algal', 'deglaze', 'deglazed',
    'eagled', 'geez', 'gelee', 'gigged', 'glia', 'zagged', 'zigged'
]

EXCLUDE_WORD_LIST = [
    'continuo', 'cony', 'coon', 'iconicity', 'initio', 'nicotinic', 'nuncio', 'toto', 'yoyo', 'eigne',
    'geeing', 'ginnie', 'whig', 'algid', 'diallage', 'gael', 'gail', 'gaza', 'geed', 'gelid', 'lege',
    'allah', 'althea', 'athena', 'ethel', 'halloo', 'hanna', 'hannah', 'helen', 'helena', 'leah',
    'loth', 'nathan', 'noah', 'othello'
]


def letter_check(word: str, letter_list: list) -> bool:
    """Checks if every character in a word is in our letter list."""
    check_list = [letter in letter_list for letter in word]
    return all(check_list)

def display_word_column(
    column: st.delta_generator.DeltaGenerator,
    word_list: list,
    start_index: int,
    end_index: int
) -> None:
    """Display part of a list as a column of words."""
    with column:
        for word in word_list[start_index: end_index]:
            st.write(word)
    
    
#1. READ IN WORDS WITH INITIAL CLEANING
df_all = pd.read_csv('data/words.csv')
df_all['word_length'] = df_all.word.str.len()

# filter out words under 4 letters or in the exclude list
df_all = df_all[(df_all.word_length >= 4) & (~df_all.word.isin(EXCLUDE_WORD_LIST))].copy()

# add words from the custom list
df_all = pd.concat((
    df_all, pd.DataFrame(ADDED_WORD_LIST, columns=['word'])
))

#2. STREAMLIT HEADERS
st.title("NYT Spelling Bee App")
st.write("The rules of Spelling Bee are simple: you are given 7 letters to make words. One of these letters must be included in every word and all words must only consist of this letter plus some of the other 6. Words must be four letters or longer. Each day, there are 1+ pangram(s), which include all 7 letters.") 

st.write("It is worth noting that this is NOT the same source of words the New York Times uses, so the lists this script may output certain words that are not accepted by the game, and could potentially miss some used by the NY Times. I am unable to find the list that they use. If you see a word that the game won't accept or a word missing from this list, please let me know!")
    
st.write("To play the game, go to this link: https://www.nytimes.com/puzzles/spelling-bee. Obviously, I would consider using this app as a form of cheating (but I won't tell.)")

#3. INPUT LETTERS FOR DAY'S SPELLING BEE 
st.header('Letter Selection')

alphabet_list = list(string.ascii_lowercase)
middle_letter = st.selectbox("Choose Middle Letter", alphabet_list) #user inputs middle letter

# start the list of letters with the middle letter
all_letters = [middle_letter]

#add each letter to our list of all letters
others = st.multiselect("Choose All Other Letters", alphabet_list) #user inputs other letters
all_letters += others
    

if len(others) != 6:
    st.write('Please Choose 6 Additional Letters', color='red')   
else:    
    # 4. NARROW DOWN WORD LIST
    df_middle_letter = df_all[df_all.word.str.contains(middle_letter)].copy()

    #make a column for words containing every letter
    for i in range(6):
        df_middle_letter[i] = df_middle_letter.word.str.contains(others[i])    
    df_middle_letter['all'] = (
        df_middle_letter[0] & df_middle_letter[1] &
        df_middle_letter[2] & df_middle_letter[3] &
        df_middle_letter[4] & df_middle_letter[5]
    )

    #apply this function to our list and then shrink dataframe to only have allowed words
    df_middle_letter['check'] = df_middle_letter['word'].apply(lambda x: letter_check(word=x, letter_list=all_letters))
    df_final = df_middle_letter[df_middle_letter['check']].copy()

    # 5. RESULTS
    st.header("Today's Pangram(s):")
    pangrams = df_final[df_final['all']]['word'].to_list()
    for pangram in pangrams:
        st.subheader(pangram)
    
    n_words = df_final.shape[0]  
    n_words_4 = np.ceil(n_words/4).astype(int)

    st.header(f"Full List of Words (total={n_words}):")
    words = df_final['word'].to_list()

    col1, col2, col3, col4 = st.columns(4)
    display_word_column(col1, words, 0, n_words_4)
    display_word_column(col2, words, n_words_4, 2 * n_words_4)
    display_word_column(col3, words, 2 * n_words_4, 3 * n_words_4)
    display_word_column(col4, words, 3 * n_words_4, n_words)
