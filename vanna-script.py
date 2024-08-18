import time

import streamlit as st

# --- Vanna setup ---
from vanna.remote import VannaDefault

vanna_model_name = st.secrets.vanna.model
vanna_api_key = st.secrets.vanna.api_key
vn = VannaDefault(model=vanna_model_name, api_key=vanna_api_key)

vn.connect_to_postgres("localhost", user="postgres", password="master", dbname="vanna-test", port=5432)


def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages rom history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What's up?"):
    # Add user prompt to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user in chat msg container
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        sql = vn.generate_sql(prompt)
        stream = st.write(sql)
        df = vn.run_sql(sql)
        st.dataframe(df, use_container_width=True)
        code = vn.generate_plotly_code(question=prompt, sql=sql, df=df)
        fig = vn.get_plotly_figure(plotly_code=code, df=df)
        st.plotly_chart(fig, use_container_width=True)

    st.session_state.messages.append({"role": "assistant", "content": sql})