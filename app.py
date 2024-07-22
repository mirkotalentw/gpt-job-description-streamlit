import re
from openai import OpenAI
import os
import streamlit as st
from dotenv import load_dotenv
import json
from pydantic import BaseModel, validator
from typing import List, Optional
import requests
 
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
 
# Make sure you have the API key in the environment variable; otherwise, this will be None.
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable not found.")
 
# Set the API key for the OpenAI client
OpenAI.api_key = openai_api_key
 
# openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()

system_instruction = """
You are a recruiter for a tech company. You are writing a job description for a new position. The job description must be written on {APPLICATION_LANGUAGE}.
The job title will be provided by the user. Please write a job description based on the job title with following requirements:
The main duties and responsibilities should be described unambiguously and in detail. According to a StepStone survey, only 42 per cent of candidates feel that job descriptions outline duties and responsibilities in a way that gives a clear picture of the role.
Describe the role in as much detail as possible:
Use keywords to describe the role in five to eight bullet points
Establish a hierarchy of duties by starting with the most important ones and ending with more minor details
Round off the section with information on strategic topics, the level of operational responsibility and/or current projects
The job description should be written in a way that is easy to understand and free of jargon. It should be tailored to the target group and should not contain any unnecessary information. Also, should not be too long or too short (it should contain in range 200-250 words).
It should NOT CONTAINT the summary at the end.
Do not include  any information about the company or the team in the job description. Do not include about project or company culture.
"""

system_instruction_2 = """
You are a recruiter for a tech company. You are writing a requirement profile for a new position. The requirement profile must be written on {APPLICATION_LANGUAGE}.
The job title will be provided by the user. Please write a requirements based on the job title with following requirements:
The required specialist knowledge and the desired qualifications (vocational or academic) must be clearly stated in the requirements profile.
At the very least, you should describe the qualification(s) needed and the specialist knowledge relevant to the position
Indicate how much professional experience you expect the ideal candidate to have
If no qualifications or prior knowledge are required, make this clear
Clearly state which requirements are essential and which are merely desirable
Once again, it is important to avoid the usual buzzwords such as ‘team-oriented’, ‘communicative’ and ‘able to work under pressure’. There are very few positions for which these skills are not required. Instead, you should try to define – as a team, if possible – which specific skills are genuinely important for the vacancy in question.
Always remember that applicants will be discouraged if the requirements are too high or too low. It’s all about striking the right balance.
The requirements should be written in a way that is easy to understand and free of jargon. It should be tailored to the target group and should not contain any unnecessary information. Also, should not be too long or too short (it should contain around 200 words).
It should NOT CONTAINT the summary at the end. 
"""


def check_credentials(username, password):
    correct_password = os.getenv('USER_PASSWORD')
    return username == "talentwunder" and password == correct_password


if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    
    
def display_login_form():
    st.title("Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")
        if login_button:
            if check_credentials(username, password):
                st.session_state.logged_in = True
                st.success("Logged in successfully.")
                # Using st.experimental_rerun() to force the app to rerun might help, but use it judiciously.
                st.experimental_rerun()
            else:
                st.error("Incorrect username or password.")  

                
                
def display_main_app():
    st.title('AI Job Description Generator')
    selected_model = "gpt-4o"
    selected_lang = st.selectbox(
    "Application language:",
    ("en", "de"))
    user_input = st.text_input("Enter your job title:")
    if selected_lang == "de":
        language = "German"
    else:
        language = "English"

 
    if st.button('Generate Job Description'):
        if user_input:
            with st.spinner('Generating text... Please wait'):
                completion = client.chat.completions.create(
                  model='gpt-4o',
                  temperature=0,
                  messages=[
                    {"role": "system", "content": system_instruction.replace("{APPLICATION_LANGUAGE}", language)},
                    {"role": "user", "content": user_input},
                ])
    
                result = completion.choices[0].message.content  
                st.write(result)
                
    if st.button('Generate Job Requirement Profile'):
        if user_input:
            with st.spinner('Generating text... Please wait'):
                completion = client.chat.completions.create(
                  model='gpt-4o',
                  temperature=0,
                  messages=[
                    {"role": "system", "content": system_instruction_2.replace("{APPLICATION_LANGUAGE}", language)},
                    {"role": "user", "content": user_input},
                ])
    
                result = completion.choices[0].message.content  
                st.write(result)
                
 
if not st.session_state.logged_in:
    display_login_form()
else:
    display_main_app()