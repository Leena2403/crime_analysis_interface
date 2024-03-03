import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import seaborn as sns

crime_type = ['Crimes Against Women', 'Crimes Against Children', 'Theft', 'Crimes Against SC/ST', 'Serious Fraud','Juvenile Crime']
# Read crime data
df = pd.read_csv("Datasets/42_District_wise_crimes_committed_against_women_2001_2012.csv")
df = df[df['STATE/UT'] == 'KARNATAKA']
df_yearly = df.groupby(['DISTRICT', 'Year']).sum().reset_index()
df_yearly['Total Crimes'] = df_yearly.iloc[:, 3:].sum(axis=1)
df_yearly = df_yearly.drop(columns=['Rape', 'Dowry Deaths', 'Kidnapping and Abduction',
                                    'Assault on women with intent to outrage her modesty',
                                    'Insult to modesty of Women', 'Cruelty by Husband or his Relatives',
                                    'Importation of Girls'])

data_yearly = df.groupby(['DISTRICT', 'Year']).sum().reset_index()
# dropping the row "Total"
districts_drop = ['TOTAL']
df_dropped_total = df_yearly.drop(index=districts_drop,errors='ignore')
districts_to_drop = ['TOTAL']
df_dropped_total = df_dropped_total[~df_dropped_total['DISTRICT'].isin(districts_to_drop)]

# Read geographical data
data = pd.read_csv("Datasets/data_12.csv")
data.dropna(inplace=True)

#For correlation map
df_stat = pd.read_csv("Datasets/stat_file.csv")

def corr_mat():
    correlation_matrix = df_stat.corr()
    fig, ax = plt.subplots(figsize=(10, 8))  # Create figure and axes objects
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)  # Pass ax argument to sns.heatmap()
    ax.set_title('Correlation Matrix')  # Set title using ax.set_title()
    st.pyplot(fig)

# Function to map weight values to colors in the VIBGYOR spectrum
def map_weight_to_color(weight):
    normalized_weight = (weight - data['Total'].min()) / (data['Total'].max() - data['Total'].min())
    color = 'rgb({}, {}, {})'.format(int(255 * normalized_weight), 0, int(255 * (1 - normalized_weight)))
    return color

def display_bar_graph(df_district):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(df_district["Year"], df_district['Total Crimes'])
    ax.set_xlabel('Year')
    ax.set_ylabel('Total Crimes Against Women')
    ax.set_title(f'Total crimes against Women in {df_district}')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True)
    st.pyplot(fig)

def display_line_chart(df_district):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df_district["Year"], df_district['Total Crimes']);
    ax.set_xlabel('Year')
    ax.set_ylabel('Total Crimes Against Women')
    ax.set_title(f'Total crimes against Women in {df_district}')
    ax.tick_params(axis='x', rotation=45);
    ax.grid(True)
    st.pyplot(fig)

def total_district(data):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(data['DISTRICT'], data['Total'])
    plt.xticks(rotation='vertical');
    ax.set_xlabel('Districts')
    ax.set_ylabel('Total Crimes Against Women')
    ax.set_title(f'Total crimes against Women in Karnataka')
    ax.tick_params(axis='x', rotation=90);
    ax.grid(True)
    st.pyplot(fig)


def plot_yearly_data_total(df, start_year, end_year):
    fig, ax = plt.subplots(figsize=(12, 6))
    for year in range(start_year, end_year + 1):
        df_year = df[df['Year'] == year].reset_index()
        plt.plot(df_year['DISTRICT'], df_year['Total Crimes'], label=str(year))

    ax.set_xlabel('Year')
    ax.set_ylabel('Total Crimes Against Women')
    ax.set_title(f'Total crimes against Women in Karnataka')
    ax.tick_params(axis='x', rotation=90)
    ax.grid(True)
    ax.legend()

    # Display the plot using Streamlit
    st.pyplot(fig)


# Streamlit app
st.title('Predictive Crime Analytics')

selected_district_name = st.selectbox(
    'Select a district from Karnataka! We will show you relevant crime data ',
    df_yearly['DISTRICT'].unique()
)

selected_crime = st.selectbox(
    "Select Crime Type",
    crime_type
)

if st.button('Show Results'):

    if selected_district_name == 'TOTAL':
        total_district(data)
        m = folium.Map(location=[15.3173, 75.7139], zoom_start=7)

        heatmap_layer = HeatMap(data[['Latitude', 'Longitude', 'Total']].values.tolist(),
                                radius=10, blur=5, max_zoom=13, gradient={0.0: 'violet', 1.0: 'red'}, opacity=0.3)
        m.add_child(heatmap_layer)
        folium_static(m)

    else:
        df_district = df_yearly[df_yearly['DISTRICT'] == selected_district_name]
        display_bar_graph(df_district)
        display_line_chart(df_district)

        # Get geographical coordinates of the selected district
        district_coords = data[data['DISTRICT'] == selected_district_name][['Latitude', 'Longitude']].values.tolist()[0]

        m = folium.Map(location=[15.3173, 75.7139], zoom_start=7)

        heatmap_layer = HeatMap(data[['Latitude', 'Longitude', 'Total']].values.tolist(),
                            radius=10, blur=5, max_zoom=13, gradient={0.0: 'violet', 1.0: 'red'}, opacity=0.3)
        m.add_child(heatmap_layer)

        # Add marker for the selected district
        folium.Marker(location=district_coords, popup=selected_district_name,
           icon=folium.Icon(color='green')).add_to(m)

        folium_static(m)

if selected_district_name == 'TOTAL':
    start_year = st.number_input("Start Year", value=2001, min_value=2001, max_value=2012, step=1)
    end_year = st.number_input("End Year", value=2012, min_value=start_year, max_value=2012, step=1)

    # Button to plot yearly data
    if st.button("Plot Yearly Data"):
        plot_yearly_data_total(df_dropped_total, start_year, end_year)

if st.button('Show Correlation Matrix'):
    corr_mat()