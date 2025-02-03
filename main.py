import streamlit as st
import pandas as pd

from func.trip_analysis import tripcounter
from func.visualizer import heatmap, markov_graph, route_map


st.title('NYC Taxi Trip Analysis')
st.write('This is the experimental project using spatial data to map the mobility of taxi customers in New York based on secondary data from Kaggle. The data acquired consist of the origin and destination location in latitude and longitude that correspond to particular taxi’s ID number. The objective is to find the NYC people probability to move from one location to another, which can be used for traffic regulation or public transportation improvement.') 
st.write('The reverse geocode technique was needed to enable municipality/borough’s name identification and travel route. Since it took long time to reverse geocode, the preprocessed and projected data then separated and saved into sub-folder inside data folder. The transition matrix was created in order to understand the mobility pattern among boroughs in New York, United States. The transition matrix then visualized in chord diagram which shows the mobility both between and within areas.') 
st.write('In this project I used several libraries for spatial data analysis such as OSMNX (open-source map network), networkx, geocode, pandas, holoviews (due to bokeh incompatibility to streamlit, the chord diagram cannot be shown).')

url = "./data"
df = pd.read_csv(url+'/raw_sample.csv')

st.write('Dataset source: https://www.kaggle.com/datasets/elemento/nyc-yellow-taxi-trip-data')
st.write(df)


st.subheader('Geocode to Geohash Conversion')
st.write('The Geocode (latitude and longitude) was reversed to Geohash format using reverse-geocode for each trip. Also returned the municipality/borough name, which will be used to calculate transition probability between two location.')
col1, col2 = st.columns(2)

df_pickup = pd.read_csv(url+'/projected_coordinate/pickup_data.csv')
df_dropoff = pd.read_csv(url+'/projected_coordinate/dropoff_data.csv')

col1.subheader("Pickup Details")
col1.dataframe(df_pickup)

col2.subheader("Dropoff Details")
col2.dataframe(df_dropoff)


# Dataframe operation
df_pickup.rename(columns={'name':'name_orig','admin':'admin_orig','admin2':'admin2_orig', 'geohash': 'node_orig'}, inplace=True)
df_dropoff.rename(columns={'name':'name_dest','admin':'admin_dest','admin2':'admin2_dest', 'geohash': 'node_dest'}, inplace=True)
df_concat = pd.concat([df, df_pickup.iloc[:,2:], df_dropoff.iloc[:,2:]], axis = 1)

df_trip = tripcounter(df_concat, "name_orig", "name_dest")
df_trip_sorted = df_trip.sort_values(by='freq', ascending=False)
df_trip_sorted.rename(columns={'level_0': 'pickup', 'level_1': 'dropoff', 'freq': 'frequency'}, inplace=True)
df_trip_sorted["probability"] = df_trip_sorted["frequency"] / df_trip_sorted["frequency"].sum()
df_trip_sorted.reset_index(drop=True, inplace=True)



st.subheader("Transition Probability Among Cities")
st.write('The identified municipalities/boroughs from pickup and dropoff locations are then used to determine the frequency and probability of each trip. In Markov model, this trip is viewed as transition from one state to another.')
st.dataframe(df_trip_sorted, use_container_width=True)
st.write('The transition probability is then visualized in transition matrix heatmap to make us easier in identifying which transition (in this case is people mobility) that is most likely to happen.')
st.pyplot(heatmap(df_trip_sorted))

st.subheader('Markov Transition Visualization')
number = st.number_input(
    "Insert a number (top-N trip) to visualize", min_value=1, max_value=len(df_trip_sorted), value=10, step=1, placeholder='insert number .. (min: 1, max: 314)')
df_toptrip = df_trip_sorted.head(number)
df_toptrip.reset_index(drop=True, inplace=True)

if st.button(label='Show graph'):
    st.write('Markov transition graph from top-', number, ' trip')
    st.pyplot(markov_graph(df_toptrip))



st.subheader('Route Map Visualization')
number = st.number_input(
    "Insert value (row index)", min_value=0, max_value=len(df), value=5, step=1, placeholder='insert number .. (min: 1, max: 314)')

location = 'New York City, USA'
origin = df_pickup.iloc[number,-1]
destination = df_dropoff.iloc[number,-1]

col1, col2 = st.columns(2)
col1.subheader("Pickup Details")
col1.dataframe(df_pickup.loc[number])

col2.subheader("Dropoff Details")
col2.dataframe(df_dropoff.loc[number])

if st.button(label='Show route'):
    st.pyplot(route_map(location, origin, destination))
