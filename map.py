import streamlit as st
import pandas as pd
from keplergl import KeplerGl
from streamlit_keplergl import keplergl_static

csv_path = 'cleaned_properties_with_coordinates.csv'
df = pd.read_csv(csv_path)

st.sidebar.header("Filter and Sort Options")

num_properties = st.sidebar.slider("Number of properties to display", 100, 200, 20)

sort_by = st.sidebar.selectbox("Sort properties by", options=["Address", "Opening", "Closing"])

min_opening, max_opening = st.sidebar.slider("Filter by opening bid (in dollars)", 0, int(df["Opening"].fillna(0).max()), (1000, 50000))

df_filtered = df[df["Opening"].fillna(0).between(min_opening, max_opening)]
df_filtered = df_filtered.sort_values(by=sort_by).head(num_properties)

config = {
    'version': 'v1',
    'config': {
        'mapState': {
            'bearing': 0,
            'latitude': 43.1566,
            'longitude': -77.6088,
            'zoom': 12,
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

map_1 = KeplerGl(height=500, data={'properties': df_filtered}, config=config)

st.write("2024 Rochester, NY Tax Foreclosure Auction")
keplergl_static(map_1)

st.write(f"Displaying {len(df_filtered)} properties:")
st.dataframe(df_filtered[['Address', 'Opening', 'Closing', 'Latitude', 'Longitude']])