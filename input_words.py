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

mode = ['append','view']

finder = ['english word','հայերէնի բար','pronounciation']

df = pd.read_csv('western_armenian_words.csv')

user_mode = st.selectbox("Please select the mode you want to work in:", mode)



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

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df


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

if user_mode == 'view':

    search = st.selectbox("Would you like to search for a specific word or filter the table?",['specific word','table'])

    if search == 'specific word':
        word_finder = st.selectbox("How would you like to search for the word?",finder)

        if word_finder == 'english word':
            word = st.text_input("Please enter the word you would like to edit")
            if st.button('find word'):
                i = df.loc[df['english'] == word]
                st.write(i)

        elif word_finder == 'հայերէնի բար':
            word = st.text_input("Please enter the word you would like to edit")
            if st.button('find word'):
                i = df.loc[df['հայերէն'] == word]
                st.write(i)

        elif word_finder == 'pronounciation':
            word = st.text_input("Please enter the word you would like to edit")
            if st.button('find word'):
                i = df.loc[df['pronounciation'] == word]
                st.write(i)
    if search == 'table':
        # modification_container = st.container()
        # with modification_container:
        #     to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        # for column in to_filter_columns:
        #     left, right = st.columns((1, 20))
        #     left.write("↳")
        #     if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
        #         user_cat_input = right.multiselect(
        #             f"Values for {column}",
        #             df[column].unique(),
        #             default=list(df[column].unique()),
        #         )
        #         df = df[df[column].isin(user_cat_input)]
        
        # st.dataframe(filter_dataframe(df))
        st.dataframe(df)
