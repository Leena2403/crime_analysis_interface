#This is being created by Souryadeepta Majumdar (Team Data Dragons)
# This is a part of code used by Team Data Dragons for Karnataka State Police Datathon 2.0

import pandas as pd
import folium
from folium.plugins import HeatMap

data = pd.read_csv("Datasets/data_12.csv")
data.dropna(inplace=True)


# Function to map weight values to colors in the VIBGYOR spectrum
def map_weight_to_color(weight):
    # Normalizing the weight values between 0 and 1
    normalized_weight = (weight - data['Total'].min()) / (data['Total'].max() - data['Total'].min())

    # Map normalized weight to a color in the VIBGYOR spectrum
    color = 'rgb({}, {}, {})'.format(int(255 * normalized_weight), 0, int(255 * (1 - normalized_weight)))
    return color

# Creating a Folium map centered on Karnataka
m = folium.Map(location=[15.3173,75.7139], zoom_start=10)

# Adding a heatmap layer using the weight column from the dataset and mapping the weight values to colors
heatmap_layer = HeatMap(data[['Latitude', 'Longitude', 'Total']].values.tolist(),
                        radius=10, blur=5, max_zoom=13, gradient={0.0: 'violet', 1.0: 'red'})
m.add_child(heatmap_layer)

# Saving the map as an HTML file
m.save('heat.html')



