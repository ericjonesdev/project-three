import os
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd 
import streamlit as st 
import plotly.express as px 
from PIL import Image



CREDS_FILE = os.getenv("CREDS")

if CREDS_FILE:
    CREDS = Credentials.from_service_account_file(CREDS_FILE)
else:
    # Handle the case where the CREDS_FILE environment variable is not set
    pass


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


#SET PAGE CONFIGURATION PARAMETERS FOR LOCAL GOOGLE SPREADSHEET FILE
st.set_page_config(page_title='Survey Results 2022')
st.header('Survey Results 2022')
st.subheader('Data Analysis At Your Fingertips')


# Load the data from the spreadsheet into a Pandas dataframe
excel_file = 'Survey_Results.xlsx'
sheet_name = 'DATA'
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# Select the columns to use in the scatter plot
x = df['Unnamed: 1']
y = df['Unnamed: 2']
z = df['Unnamed: 3']

# Create the scatter plot
fig = px.scatter_3d(x=x, y=y, z=z)

# Display the scatter plot in Streamlit
st.plotly_chart(fig)


# Add some formatted text to the page
st.markdown('# Data Analysis Results')
st.markdown('Here are the results of our data analysis:')
st.markdown('**Total Number of Participants:** {}'.format(df.shape[0]))
most_popular_rating = df['Unnamed: 3'].mode()[0]
st.markdown('The most popular rating is {}'.format(most_popular_rating))
print(df.columns)


# --- LOAD THE DATAFRAME
excel_file = 'Survey_Results.xlsx'
sheet_name = 'DATA'

df = pd.read_excel(excel_file,
                   sheet_name=sheet_name,
                   usecols='B:D',
                   header=3)

df_participants = pd.read_excel(excel_file,
                                sheet_name= sheet_name,
                                usecols='F:G',
                                header=3)
df_participants.dropna(inplace=True)

# --- STREAMLIT SELECTION
department = df['Department'].unique().tolist()
ages = df['Age'].unique().tolist()

age_selection = st.slider('Age:',
                        min_value= min(ages),
                        max_value= max(ages),
                        value=(min(ages),max(ages)))

department_selection = st.multiselect('Department:',
                                    department,
                                    default=department)

# --- FILTER DATAFRAME BASED ON SELECTION
mask = (df['Age'].between(*age_selection)) & (df['Department'].isin(department_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_result}*')

# --- GROUP DATAFRAME AFTER SELECTION
df_grouped = df[mask].groupby(by=['Rating']).count()[['Age']]
df_grouped = df_grouped.rename(columns={'Age': 'Votes'})
df_grouped = df_grouped.reset_index()

# --- PLOT BAR CHART
bar_chart = px.bar(df_grouped,
                   x='Rating',
                   y='Votes',
                   text='Votes',
                   color_discrete_sequence = ['#9965D5']*len(df_grouped),
                   template= 'plotly_white')
st.plotly_chart(bar_chart)

# --- DISPLAY IMAGE & DATAFRAME
col1, col2 = st.columns(2)
image = Image.open('images/survey.png')
col1.image(image,
        caption='Your Data Your Way',
        use_column_width=True)
col2.dataframe(df[mask])

# --- PLOT PIE CHART
pie_chart = px.pie(df_participants,
                title='Total No. of Participants',
                values='Participants',
                names='Departments')

st.plotly_chart(pie_chart)




