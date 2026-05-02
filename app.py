import os
import requests
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

st.title("Equipment Return Dashboard")

SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL", "")).strip()
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY", "")).strip()
SUPABASE_URL = SUPABASE_URL.replace("/rest/v1/", "").replace("/rest/v1", "")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Missing Supabase credentials.")
    st.stop()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.subheader("Seattle Weather API")
try:
    weather_url = "https://api.open-meteo.com/v1/forecast?latitude=47.61&longitude=-122.33&daily=temperature_2m_max&timezone=America%2FLos_Angeles"
    weather_response = requests.get(weather_url, timeout=10)
    assert weather_response.status_code == 200
    weather_data = weather_response.json()
    assert "daily" in weather_data
    assert "temperature_2m_max" in weather_data["daily"]
    st.write("Weather API connected successfully.")
except Exception:
    st.warning("Weather API unavailable.")

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
    st.divider()
st.header("GIX Events Browser")

try:
    events_response = supabase.table("events").select("*").order("event_date").execute()
    events = events_response.data

    assert isinstance(events, list)

    if len(events) > 0:
        assert "event_name" in events[0]
        assert "event_date" in events[0]
        assert "location" in events[0]

except Exception as e:
    st.error("Could not load events.")
    st.write(e)
    events = []

location_filter = st.selectbox(
    "Filter events by location",
    ["All"] + sorted(list(set(event["location"] for event in events)))
)

if location_filter == "All":
    filtered_events = events
else:
    filtered_events = [
        event for event in events
        if event["location"] == location_filter
    ]

if len(filtered_events) == 0:
    st.write("No events found.")
else:
    for event in filtered_events:
        st.subheader(event["event_name"])
        st.write(f"Date: {event['event_date']}")
        st.write(f"Location: {event['location']}")
        st.write("---")
