import os
import streamlit as st
import openai
import datetime
from contextlib import redirect_stdout

oa = openai
openai.api_key = st.secrets["OPENAI_API_KEY_QX"]
result = "_Submit your SQL code and result will appear here_"

def get_converted_code(myprompt,persona):
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=[
            {"role": "system", "content": persona},
            {"role": "user", "content": myprompt},
        ]
    )
    return response.choices[0].message.content

persona = "You are an expert full-stack data engineer who is adept at manipulating data with SQL (all flavors) as well as with Python (especially Pandas). You often help data analysts convert their SQL into Python. Sometimes the SQL is very complex, or references external tools such as SQL statements that are intended for use in Apache Flink. You do your best to find the nearest equivalent but you are not afraid to point out aspects that do not translate well into Pandas."

with st.form(key="sqlpandas"):
        st.markdown(f'### SQL Query')
        st.markdown(f'Enter an SQL Query and the tool will do its best to convert the query into Pandas syntax')
        sqlcode = st.text_area('SQL Query:', height=200)

        gpt4prompt = f"Please analyze the following SQL query and do your best to convert it into Python pandas syntax.\n{sqlcode}\nPlease enclose the code in markdown syntax for code blocks like this ```python\n<code/>\n```. If you have any comments, please add them after the code block."

        submit_form = st.form_submit_button(label='Convert')

        # if the submit button is pressed, send the whole prompt to OpenAI
        if submit_form:
            with st.spinner("Generating code..."):
                result = get_converted_code(gpt4prompt,persona)
                print(result)
            st.success('Done!')

        st.markdown(f'_Your SQL code will be repeated here for comparison._')
        st.markdown(f'```sql\n{sqlcode}\n```')

        st.markdown(f'### Pandas Code')
        st.markdown(f'{result}')

