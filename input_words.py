#### Western Armenian Word Input Tool ####
#### by Tori Davis ####

##############################################################################

#### Import Libraries ####

import streamlit as st
import pandas as pd
from csv import writer
import numpy as np

##############################################################################

##### Page Set Up #####

# set up page name
st.set_page_config(page_title="western armenian word input tool", page_icon="🇦🇲")
# set up title on the web application
st.title("western armenian word input tool")
st.header("tool for tori to add new armenian words as they learn them :)")

##############################################################################

categories = {

    'beings':       ['people','family','animals'],
    'food':         ['drinks','vegetables','fruit','grains','spices',
                     'protein','general','uncategorized','dishes'],
    'things':       ['nature','music','clothes','toys','kitchen',
                     'body parts','general','non-physical'],
    'time':         ['months','days','time','general'],
    'other':        ['weather','colors','numbers','rank'],
    'places':       ['countries','continents','armenian places',
                     'general','directions'],
    'verbs':        ['infinative verbs','present tense','past tense',
                     'future tense','past perfect tense','imperative verb',
                     'irregular conjugation'],
    'descriptions': ['size','quantity','quality','behavior']
              }

#### Append to CSV ####

category = st.selectbox("Please select the word category",categories.keys())
subcategory = st.selectbox("Please select the word subcategory",categories[category])
english = st.text_input('Please enter the word in english - for example: cat')
pronounciation = st.text_input('Please enter the pronounciation of the word - for example: gadoo')
հայերէն = st.text_input('Please enter the word in հայերէն - for example: կատու')


newEntry = [category, subcategory, english, հայերէն, pronounciation]

if st.button('save word'):
    with open('western_armenian_words.csv','a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(newEntry)
        f_object.close()
    st.write('word has been saved')

df = pd.read_csv('western_armenian_words.csv')
st.write(df.sort_values(['category','subcategory','english']))