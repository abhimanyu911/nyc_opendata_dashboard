import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px


st.title("Motor vehicle collisions in New York City")
st.markdown("This application is a Streamlit dashboard that can be used "
	"to analyze motor vehicle collisions in NYC 🚗💥")

@st.cache(ttl=3600*24, show_spinner=False)
def load_data(nrows):
	data = pd.read_csv('data.csv',nrows=nrows,parse_dates=[["CRASH DATE","CRASH TIME"]])
	data.dropna(subset=['LATITUDE','LONGITUDE'],inplace=True)
	lowercase = lambda x: str(x).lower()
	data.rename(lowercase,axis='columns',inplace=True)
	strip_spaces = lambda x:str(x).replace(" ","_")
	data.rename(strip_spaces,axis='columns',inplace=True)
	data.rename(columns={'crash_date_crash_time':'date/time'},inplace=True)
	return data

orig_data = load_data(40000)

st.header("Where do most people get injured in NYC?")
injured_people = st.slider("No. of persons injured in vehicle accidents",0,10)
st.map(orig_data.query("number_of_persons_injured >= @injured_people")
		[["latitude","longitude"]].dropna(how="any"))

st.header("How many accidents occur at a particular time of the day?")
hour = st.slider("Hour to look at in 24 hr format:",0,23)
data = orig_data[orig_data['date/time'].dt.hour == hour]

st.markdown("### No of collisions between %i:00 and %i:00:" %(hour,(hour+1)%24))
st.markdown("Drag the map to look around!")

midpoints = (np.average(data['latitude']),np.average(data['longitude']))
st.write(pdk.Deck(
	map_style="mapbox://styles/mapbox/light-v9",
	initial_view_state={
		"latitude":midpoints[0],
		"longitude":midpoints[1],
		"zoom":11,
		"pitch":50,
	},
	layers=[
		pdk.Layer(
		"HexagonLayer",
		data=data[["date/time","latitude","longitude"]],
		get_position=["longitude","latitude"],
		radius=150,
		extruded=True,
		pickable=True,
		elevation_scale=4,
		elevation_range=[0,1000],
		),
	],
))

st.subheader("Breakdown by minute between %i:00 and %i:00:" %(hour,(hour+1)%24))
filtered = data[
	(data["date/time"].dt.hour >= hour) & (data["date/time"].dt.hour < (hour+1))
]
hist  = np.histogram(filtered["date/time"].dt.minute,range=(0,60),bins=60)[0]
chart_data = pd.DataFrame({'minute':range(60),'crashes':hist})
fig = px.bar(chart_data,x="minute",y="crashes",hover_data=["minute","crashes"],height=400)
st.write(fig)

st.header("Top 5 dangerous streets by affected type")
select = st.selectbox("Affected type of people",["Pedestrians","Cyclists","Motorists"])
if (select== "Pedestrians"):
	st.write(orig_data.query("number_of_pedestrians_injured >=1")
		[["on_street_name","number_of_pedestrians_injured"]].sort_values(
					by=["number_of_pedestrians_injured"],ascending=False).dropna(how="any")[:5])
elif (select== "Cyclists"):
	st.write(orig_data.query("number_of_cyclist_injured >=1")
		[["on_street_name","number_of_cyclist_injured"]].sort_values(
					by=["number_of_cyclist_injured"],ascending=False).dropna(how="any")[:5])
else:
	st.write(orig_data.query("number_of_motorist_injured >=1")
		[["on_street_name","number_of_motorist_injured"]].sort_values(
					by=["number_of_motorist_injured"],ascending=False).dropna(how="any")[:5])

if st.checkbox("Display Raw Data",False):
	st.subheader('Raw data')
	st.write(data)
