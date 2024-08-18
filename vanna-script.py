import time, os
import streamlit as st
import helpers.file_manipulation as fm
from vanna.remote import VannaDefault


@st.cache_resource
def initialize_vanna():
    vanna_model_name = st.secrets.vanna.model
    vanna_api_key = st.secrets.vanna.api_key
    vn_m = VannaDefault(model=vanna_model_name, api_key=vanna_api_key)
    postgres_secrets = st.secrets.pg
    vn_m.connect_to_postgres(
        host=postgres_secrets.host,
        user=postgres_secrets.user,
        password=postgres_secrets.password,
        dbname=postgres_secrets.db_name,
        port=postgres_secrets.port
    )
    return vn_m


@st.cache_data
def train_vanna(_vn_model):
    df_information_schema = _vn_model.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")
    plan = _vn_model.get_training_plan_generic(df_information_schema)
    _vn_model.train(plan=plan)

    ddl_info = fm.get_ddl_information()
    for ddl in ddl_info:
        _vn_model.train(ddl=ddl)


def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


vn = initialize_vanna()
train_vanna(vn)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What's up?"):
    # Add user prompt to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user input in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        sql = vn.generate_sql(prompt)
        stream = st.write(response_generator(sql))
        if not sql.startswith("The provided question is unclear"):
            df = vn.run_sql(sql)
            st.dataframe(df, use_container_width=True)
            code = vn.generate_plotly_code(question=prompt, sql=sql, df=df)
            fig = vn.get_plotly_figure(plotly_code=code, df=df)
            st.plotly_chart(fig, use_container_width=True)

    st.session_state.messages.append({"role": "assistant", "content": sql})

