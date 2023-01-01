import gspread
from google.oauth2.service_account import Credentials
import pandas as pd 
import streamlit as st 
import plotly.express as px 
from PIL import Image

# SET SCOPE FOR GOOGLE APIs
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
    "https://spreadsheets.google.com/feeds"
    ]

#DECLARE INITIAL VARIABLES
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('survey_results_sheet')

survey = SHEET.worksheet('data')

surveydata = survey.get_all_values()
print(surveydata)

#SET PAGE CONFIGURATION PARAMETERS FOR LOCAL GOOGLE SPREADSHEET FILE
st.set_page_config(page_title='Survey Results 2022')
st.header('Survey Results 2022')
st.subheader('Data Analysis At Your Fingertips')

