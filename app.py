import os
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

st.title("Equipment Return Dashboard")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Missing Supabase credentials. Check your .env file.")
    st.stop()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    response = supabase.table("equipment_returns").select("*").execute()
    data = response.data
    assert isinstance(data, list)
except Exception as e:
    st.error("Failed to fetch equipment return data.")
    st.write(e)
    st.stop()

st.subheader("All Equipment Returns")

for row in data:
    st.write(f"Student: {row['student_name']}")
    st.write(f"Equipment: {row['equipment_name']}")
    st.write(f"Due date: {row['due_date']}")
    st.write(f"Returned: {row['returned']}")
    st.write("---")