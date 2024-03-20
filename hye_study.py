#### Western Armenian Study Tool ####
#### by Tori Davis ####

##############################################################################

#### Import Libraries ####

import streamlit as st
import pandas as pd
import json
from csv import writer
import numpy as np
from random import shuffle

##############################################################################

#### Page Set Up ####

# set up page name
st.set_page_config(page_title="western armenian study tool", page_icon="🇦🇲")
# set up title on the web application
st.title("western armenian study tool")
st.header("tool for tori to review western armenian words as they learn them :)")

##############################################################################

#### Read in CSV ####

df = pd.read_csv('western_armenian_words.csv')
df['english word'] = pd.to_numeric(df['english word'], errors='ignore')

##############################################################################

#### Set Up Selection Fields ####

modes = {
    'flashcards':       ['english word','հայերէնի բար','pronounciation','q&a'],
    'typing practice':  ['english word to հայերէն','pronunciation to հայերէն','q&a']
}

with open('word_categories.json') as fp:
    categories = json.load(fp)

lesson_list = sorted(df.lesson.dropna().unique())
lesson_list = [int(x) for x in lesson_list]

##############################################################################

#### Set Up Selection Fields ####

user_mode   = st.selectbox("Please select the study mode",sorted(modes.keys()))
submode     = st.selectbox("Please select which term you want to be provided",sorted(modes[user_mode]))
filter = st.selectbox("Would you like to filter based on lesson or category?",['lesson','category'])
if filter == 'category':
    category =          st.selectbox("Please select the word category",sorted(categories.keys()))
    subcategory =       st.selectbox("Please select the word subcategory",sorted(categories[category]))
    curated_df = df[(df['category'] == category) & (df['subcategory'] == subcategory)]
elif filter == 'lesson':
    lesson_selection = st.selectbox("Choose a lesson number",lesson_list) 
    curated_df = df[(df['lesson'] == lesson_selection)]

##############################################################################

#### Study Modes ####

if submode == ('english word' or 'english word to հայերէն'):
    study_list = curated_df['english word'].tolist()

elif submode == ('pronounciation' or 'pronunciation to հայերէն'):
    study_list = curated_df['pronounciation'].tolist()

elif submode == 'հայերէնի բար':
    study_list = curated_df['հայերէնի բար'].tolist()

if st.button('start studying',key ='mode'):
    shuffle(study_list)
    st.write(study_list)
    
    

