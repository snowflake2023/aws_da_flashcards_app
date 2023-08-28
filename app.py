import streamlit as st
import streamlit.components.v1 as components
from gsheetsdb import connect
import random
import pandas

# -------------- app config ---------------

st.set_page_config(page_title="AWS Flashcards")

# ---------------- functions ----------------


# callbacks
def pick_fn():
    st.session_state.pick_clicked = True

def show_ans_fn():
    st.session_state.show_clicked = True

if "pick_clicked" not in st.session_state:
    st.session_state.pick_clicked = False

if "show_clicked" not in st.session_state:
    st.session_state.show_clicked = False

if "q_no" not in st.session_state:
    st.session_state.q_no = 0

if "q_no_temp" not in st.session_state:
    st.session_state.q_no_temp = 0

conn = connect()
@st.cache_resource
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets.public_gsheets_url

rows = run_query(
    f'SELECT * FROM "{sheet_url}"'
)

row_count = len(rows)
st.caption("**There are " + str(row_count) + " scenarios in the set.**")

col1, col2 = st.columns(2)
with col1:
    question = st.button(
    "Pick a question", on_click=pick_fn, key="Pick", use_container_width=True
        )

with col2:
    answer = st.button(
            "Show answer", on_click=show_ans_fn, key="Answer", use_container_width=True
        )

if question or st.session_state.pick_clicked:
    st.session_state.q_no = random.randint(0, row_count - 1)

    if st.session_state.show_clicked:
        st.markdown(
                f'<h1><span>{rows[st.session_state.q_no_temp].Question}</span></h1>',
               # f'<h1><span>{rows[st.session_state.q_no_temp].Question}</span></h1><h4>&mdash; Question no. {st.session_state.q_no_temp+1}</em></h4>',
            unsafe_allow_html=True,
            )
    else:
        st.markdown(
                f'<h1><span>{rows[st.session_state.q_no].Question}</span></h1><h4>&mdash; Question no. {st.session_state.q_no+1}</em></h4>',
                unsafe_allow_html=True,
            )

        st.session_state.q_no_temp = st.session_state.q_no

    if answer:
        st.success(
                rows[st.session_state.q_no_temp].Answer
            )
        st.session_state.show_clicked = False



