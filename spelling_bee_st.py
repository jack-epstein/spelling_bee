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
    

# 1. READ IN WORDS WITH INITIAL CLEANING
df_all = pd.read_csv('data/words.csv')
df_all['word_length'] = df_all.word.str.len()

# filter out words under 4 letters or in the exclude list
df_all = df_all[(df_all.word_length >= 4) & (~df_all.word.isin(EXCLUDE_WORD_LIST))].copy()

# add words from the custom list
df_added_words = pd.DataFrame(ADDED_WORD_LIST, columns=['word'])
df_all = pd.concat((df_all, df_added_words))

# 2. STREAMLIT HEADERS
st.title("NYT Spelling Bee App")
st.write(
    "The rules of Spelling Bee are simple: you are given 7 letters to make words. One of these "
    "letters must be included in every word and all words must only consist of this letter plus "
    "some of the other 6. Words must be four letters or longer. Each day, there are 1+ pangram(s), "
    "which include all 7 letters."
)

st.write(
    "It is worth noting that this is NOT the same source of words the New York Times uses, "
    "so the lists this script may output certain words that are not accepted by the game, "
    "and could potentially miss some used by the NY Times. I am unable to find the list that "
    "they use. If you see a word that the game won't accept or a word missing from this list, "
    "please let me know!"
)
    
st.write(
    "To play the game, go to this link: https://www.nytimes.com/puzzles/spelling-bee. "
    "Obviously, I would consider using this app as a form of cheating (but I won't tell.)"
)

# 3. INPUT LETTERS FOR DAY'S SPELLING BEE 
st.header('Letter Selection')

alphabet_list = list(string.ascii_lowercase)

# user inputs middle letter
middle_letter = st.selectbox("Choose Middle Letter", alphabet_list)
all_letters = [middle_letter]

# user inputs other letters
other_letters = st.multiselect("Choose All Other Letters", alphabet_list)
all_letters += other_letters

# 4. NARROW 
if len(other_letters) > 6:
    st.write('WARNING: Too many letters', color='red')
elif len(other_letters) < 6:
    st.write('Please Choose 6 Additional Letters', color='red')
else:    
    # 4. NARROW DOWN WORD LIST
    df_middle_letter = df_all[df_all.word.str.contains(middle_letter)].copy()

    # check for any words that contain every letter
    df_middle_letter['pangram'] = df_middle_letter['word'].apply(
        lambda x: all([letter in x for letter in other_letters])
    )

    # check for words that only contains letters in our list
    df_middle_letter['word_in_list'] = df_middle_letter['word'].apply(
        lambda x: all([letter in all_letters for letter in x])
    )

    df_final = df_middle_letter[df_middle_letter['word_in_list']].copy()

    # 5. RESULTS
    st.header("Today's Pangram(s):")
    pangrams = df_final[df_final['pangram']]['word'].to_list()
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
