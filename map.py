import streamlit as st
import pandas as pd
from keplergl import KeplerGl
from streamlit_keplergl import keplergl_static

# Load the CSV file containing property addresses and coordinates
csv_path = 'cleaned_properties_with_coordinates.csv'  # Adjust path as needed
df = pd.read_csv(csv_path)

# Streamlit Sidebar Controls
st.sidebar.header("Filter and Sort Options")

# Number of properties to display at once
num_properties = st.sidebar.slider("Number of properties to display", 10, 100, 20)

# Sorting options for the properties
sort_by = st.sidebar.selectbox("Sort properties by", options=["Address", "Opening", "Closing"])

# Filter properties by opening bid (user can choose a range)
min_opening, max_opening = st.sidebar.slider("Filter by opening bid (in dollars)", 0, int(df["Opening"].fillna(0).max()), (1000, 50000))

# Apply filtering and sorting based on user input
df_filtered = df[df["Opening"].fillna(0).between(min_opening, max_opening)]
df_filtered = df_filtered.sort_values(by=sort_by).head(num_properties)

# Initialize Kepler.gl map configuration
config = {
    'version': 'v1',
    'config': {
        'mapState': {
            'bearing': 0,
            'latitude': 43.1566,  # Latitude for Rochester, NY
            'longitude': -77.6088, # Longitude for Rochester, NY
            'zoom': 12,  # Adjust the zoom level
            'pitch': 0
        },
        'layers': [
            {
                'type': 'point',
                'config': {
                    'dataId': 'properties',
                    'label': 'Property Locations',
                    'color': [255, 0, 0],
                    'highlightColor': [252, 242, 26],
                    'isVisible': True,
                    'visConfig': {
                        'radius': 10,
                        'opacity': 0.8,
                    },
                },
            }
        ],
    }
}

# Initialize Kepler.gl map and add the filtered data
map_1 = KeplerGl(height=500, data={'properties': df_filtered}, config=config)

# Display the Kepler.gl map in Streamlit
st.write("Rochester, NY Property Locations using Kepler.gl")
keplergl_static(map_1)

# Display the filtered properties in a table below the map
st.write(f"Displaying {len(df_filtered)} properties:")
st.dataframe(df_filtered[['Address', 'Opening', 'Closing', 'Latitude', 'Longitude']])
