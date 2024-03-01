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
    'people': ['family','friends'],
    'food': ['drinks','vegetables','fruit'],
    'things':['nature','music']
              }

#### Append to CSV ####

category = st.selectbox("Please select the word category",categories.keys())
subcategory = st.selectbox("Please select the word subcategory",categories[category])
english = st.text_input('Please enter the word in english - for example: cat')
հայերէն = st.text_input('Please enter the word in հայերէն - for example: կատու')
pronounciation = st.text_input('Please enter the pronounciation of the word - for example: gadoo')

newEntry = [category, subcategory, english, հայերէն, pronounciation]

if st.button('save word'):
    with open('western_armenian_words.csv','a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(newEntry)
        f_object.close()
    st.write('word has been saved')

df = pd.read_csv('western_armenian_words.csv')
st.write(df.sort_values(['category','subcategory','english']))