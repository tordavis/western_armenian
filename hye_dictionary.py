#### Western Armenian Word Input Tool ####
#### by Tori Davis ####

##############################################################################

#### Import Libraries ####

import streamlit as st
import pandas as pd
from csv import writer
import numpy as np
from tempfile import NamedTemporaryFile
import shutil
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

##############################################################################

#### Page Set Up ####

# set up page name
st.set_page_config(page_title="western armenian dictionary", page_icon="🇦🇲")
# set up title on the web application
st.title("western armenian dictionary")
st.header("tool for tori to review western armenian words as they learn them :)")

##############################################################################

#### Read in CSV ####

df = pd.read_csv('western_armenian_words.csv')
df['english'] = pd.to_numeric(df['english'], errors='ignore')

##############################################################################

#### Define References ####

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

mode = ['append','view']

finder = ['english word','հայերէնի բար','pronounciation']

lesson_list = sorted(df.lesson.dropna().unique())
lesson_list = [int(x) for x in lesson_list]

##############################################################################

#### Set Up Dataframe Filtering Function ####

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    modification_container = st.container()
        
    with modification_container:
        category =          st.selectbox("Please select the word category",categories.keys())
        category_filter = st.multiselect("Filter within category", categories[category])

    df = df[df['subcategory'].isin(category_filter)]

    return df

##############################################################################

#### Main function ####

def main():

    user_mode = st.selectbox("Please select the mode you want to work in:", mode)

    #### Append to CSV ####

    if user_mode == 'append':
        category =          st.selectbox("Please select the word category",categories.keys())
        subcategory =       st.selectbox("Please select the word subcategory",categories[category])
        english =           st.text_input('Please enter the word in english - for example: cat')
        pronounciation =    st.text_input('Please enter the pronounciation of the word - for example: gadoo')
        հայերէն =           st.text_input('Please enter the word in հայերէն - for example: կատու')
        lesson =            st.text_input('Please enter the lesson number from class with Arvin')

        newEntry = [category, subcategory, english, հայերէն, pronounciation,lesson]

        if st.button('save word'):
            with open('western_armenian_words.csv','a') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(newEntry)
                f_object.close()
            st.write('word has been saved')

        curated_df = df[(df['category'] == category) & (df['subcategory'] == subcategory)]
        curated_df.sort_values('english')

        if st.button('refresh table'):
            st.dataframe(
            data = curated_df,
            width = 1000,
            hide_index = 1
                        )

    #### View CSV ####

    # change in dev
    # user_mode = 'view'

    if user_mode == 'view':

        search = st.selectbox("Would you like to search for a specific word or filter the table?",['specific word','table'])

        if search == 'specific word':
            word_finder = st.selectbox("How would you like to search for the word?",finder)

            if word_finder == 'english word':
                word = st.text_input("Please enter the word you would like to see")
                if st.button('find word'):
                    i = df.loc[df['english'] == word]
                    st.write(i)

            elif word_finder == 'հայերէնի բար':
                word = st.text_input("Please enter the word you would like to see")
                if st.button('find word'):
                    i = df.loc[df['հայերէն'] == word]
                    st.write(i)

            elif word_finder == 'pronounciation':
                word = st.text_input("Please enter the word you would like to see")
                if st.button('find word'):
                    i = df.loc[df['pronounciation'] == word]
                    st.write(i)
        if search == 'table':
            filter = st.selectbox("Would you like to filter based on lesson or category?",['category','lesson'])
            if filter == 'category':
                st.dataframe(
                    data = filter_dataframe(df),
                    width = 1000,
                    hide_index = 1
                    )
            if filter == 'lesson':
                lesson_selection = st.selectbox("Choose a lesson number",lesson_list)
                curated_df = df[(df['lesson'] == lesson_selection)]
                curated_df.sort_values(['category','subcategory','english'])
                st.dataframe(
                    data = curated_df,
                    width = 1000,
                    hide_index = 1
                    )

if __name__ == "__main__":
    main()