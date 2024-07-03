import streamlit as st
import pandas as pd
from scipy import stats
from streamlit_vizzu import VizzuChart, Data, Config, Style
from ipyvizzustory import Story, Slide, Step
import plotly.graph_objects as go
import plotly.express as px

# Custom CSS for styling
custom_css = """
<style>
    .stApp {
        background-image: linear-gradient(135deg, #A9F1DF, #FFBBBB);
        background-color: transparent;
        padding: 0;
    }
    .custom-title {
        font-family: 'Georgia', serif;
        font-size: 2.5rem;
        color: #ffffff;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    .stMarkdown p {
        font-family: 'Georgia', serif;
    }
    .stButton button {
        width: 100%;
        font-family: 'Georgia', serif;
    }
    .stFileUploader {
        width: 100%;
    }
    .stSidebar {
        background-color: #f8f9fa;
        padding: 20px;
    }
</style>
"""

# Set Streamlit layout to wide
st.set_page_config(layout="wide")
st.markdown(custom_css, unsafe_allow_html=True)

# Define data types
d_types = {
    "Unnamed: 0": float,
    "building_id": str,
    "meter": str,
    "timestamp": str,
    "meter_reading": float,
    "site_id": str,
    "primary_use": str,
    "square_feet": float,
    "air_temperature": float,
    "cloud_coverage": float,
    "dew_temperature": float,
    "precip_depth_1_hr": float,
    "sea_level_pressure": float,
    "wind_direction": float,
    "wind_speed": float,
    "day": float,
    "month": str,
    "hour": float,
}

# Load dataset
@st.cache_data
def load_dataset(filepath, nrows=None):
    try:
        if nrows:
            df = pd.read_csv(filepath, nrows=nrows, dtype=d_types)
        else:
            df = pd.read_csv(filepath, dtype=d_types)
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return pd.DataFrame()

# Function to preprocess data
def preprocess_data(df):
    df['z_score'] = stats.zscore(df['meter_reading'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df


def create_indicator_chart(value, title):
    fig = go.Figure(go.Indicator(
        mode = "number",
        value = value,
        title = {"text": title, 'font': {'size': 15, 'family': 'Georgia'}},
        number = {'font': {'size': 30, 'family': 'Cambria'}},
        domain = {'x': [0, 1], 'y': [0, 1]}
    ))

    fig.update_layout(
        paper_bgcolor='rgba(255, 255, 255, 0.4)',  # White background with 50% opacity
        plot_bgcolor='rgba(255, 255, 255, 0.4)',   # Plot area background with 50% opacity
        width=300, height=300
    )
    return fig

def create_story_one(filtered_df):
    data = Data()
    data.add_df(filtered_df)
    story_one = Story(data=data)
    story_one.set_size("100%", "600px")
    story_one.set_feature("tooltip", True)

    # Define the narrative with multiple slides
    # Slide 1: Overview of Meter Readings by Month
    slide1 = Slide(
        Step(
            Config(
                {
                    "x": ["month"],
                    "y": ["mean(meter_reading)"],
                    "color": "month",
                    "label": "mean(meter_reading)",
                    "title": "Overview: Mean Meter Readings by Month",
                }
            ),
            Style(
                {
                    "paddingLeft": "3em",
                    "plot": {
                        "yAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                        "xAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                        "marker": {
                            "label": {
                                "numberFormat": "prefixed",
                                "maxFractionDigits": "1",
                                "numberScale": "shortScaleSymbolUS",
                            },
                            "rectangleSpacing": None,
                            "circleMinRadius": 0.005,
                            "borderOpacity": 1,
                            "colorPalette": "#FFB3BA #FFDFBA #FFFFBA #BAFFC9 #BAE1FF #CBAACB #FFDAC1 #FF9AA2 #B5EAD7 #E2F0CB #FFB7B2 #FFDAC1",
                        },
                    },
                    "fontFamily": "Georgia", 
                }
            )
        )
    )
    story_one.add_slide(slide1)

    # Slide 2: Focus on High Consumption using Z-Score
    slide2 = Slide(
        Step(
            Config(
                {
                    "coordSystem": "cartesian",
                    "geometry": "circle",
                    "title": "Overview: High Consumption Meter Reading by Month with Z-Score > 2",
                    "x": "month",
                    "y": {
                        "set": "mean(meter_reading)",
                        "range": {"min": "auto", "max": "110%"},
                    },
                    "color": "month",
                    "lightness": None,
                    "size": None,
                    "noop": None,
                    "split": False,
                    "align": "none",
                    "orientation": "horizontal",
                    "label": None,
                    "sort": "none",
                }
            ),
            Style(
                {
                    "plot": {
                        "yAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                        "xAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
                        "marker": {
                            "label": {
                                "numberFormat": "prefixed",
                                "maxFractionDigits": "1",
                                "numberScale": "shortScaleSymbolUS",
                            },
                            "rectangleSpacing": 0,
                            "circleMinRadius": 0.02,
                            "borderOpacity": 1,
                            "colorPalette": "#FFB3BA #FFDFBA #FFFFBA #BAFFC9 #BAE1FF #CBAACB #FFDAC1 #FF9AA2 #B5EAD7 #E2F0CB #FFB7B2 #FFDAC1",
                        },
                    },
                    "fontFamily": "Georgia",   
                }
            ),
            Data.filter("record['z_score'] > 2"),
        )
    )
    story_one.add_slide(slide2)
    return story_one

def create_donut_chart(high_consumption_percentage, low_consumption_percentage):
    fig = go.Figure(data=[go.Pie(
        labels=['High Consumption', 'Low Consumption'],
        values=[high_consumption_percentage, low_consumption_percentage],
        hole=.6,
        marker_colors=['#FF9999', '#99CC99'],
        textinfo='none'
    )])

    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(
                family="Georgia",
                size=12,
                color="black"
            )
        ),
        annotations=[dict(text=f'{high_consumption_percentage:.1f}%', x=0.18, y=0.5, font_size=15, showarrow=False, font=dict(family="Georgia")),
                     dict(text=f'{low_consumption_percentage:.1f}%', x=0.82, y=0.5, font_size=15, showarrow=False, font=dict(family="Georgia"))],
        margin=dict(l=20, r=20, t=20, b=10),  # Smaller size
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot area
        width=300,
        height=300
    )

    return fig


def create_additional_charts(filtered_df):
    charts = []

    # Scatter Plot: Meter Reading vs. Air Temperature
    fig_scatter = px.scatter(filtered_df, x='air_temperature', y='meter_reading', 
                             color='primary_use', 
                             hover_data=['building_id', 'site_id', 'square_feet'],
                             title='Meter Reading vs. Air Temperature')
    fig_scatter.update_layout(
        font_family="Georgia",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        coloraxis_colorbar=dict(titlefont=dict(family="Georgia")),
        title_font=dict(size=20, family='Georgia', color='black')
    )
    charts.append(fig_scatter)

    # Line Chart: Meter Reading Over Time
    fig_line = px.line(filtered_df, x='timestamp', y='meter_reading', 
                       color='building_id',
                       title='Meter Reading Over Time')
    fig_line.update_layout(
        font_family="Georgia",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        coloraxis_colorbar=dict(titlefont=dict(family="Georgia")),
        title_font=dict(size=20, family='Georgia', color='black')
    )
    charts.append(fig_line)

    # Histogram: Distribution of Meter Reading
    fig_histogram = px.histogram(filtered_df, x='meter_reading', 
                                 nbins=50, 
                                 title='Distribution of Meter Reading')
    fig_histogram.update_layout(
        font_family="Georgia",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font=dict(size=20, family='Georgia', color='black')
    )
    charts.append(fig_histogram)

    # Parallel Coordinates Plot
    fig_parallel = px.parallel_coordinates(filtered_df, 
                                           dimensions=['air_temperature', 'cloud_coverage', 'dew_temperature', 
                                                       'precip_depth_1_hr', 'sea_level_pressure', 'wind_speed', 
                                                       'meter_reading'],
                                           color='meter_reading',
                                           title='Parallel Coordinates Plot')
    fig_parallel.update_layout(
        font_family="Georgia",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font=dict(size=20, family='Georgia', color='black')
    )
    charts.append(fig_parallel)

    # Scatter Matrix Plot
    fig_scatter_matrix = px.scatter_matrix(filtered_df, 
                                           dimensions=['air_temperature', 'cloud_coverage', 'dew_temperature', 
                                                       'precip_depth_1_hr', 'sea_level_pressure', 'wind_speed', 
                                                       'meter_reading'],
                                           color='primary_use',
                                           title='Scatter Matrix of Variables')
    fig_scatter_matrix.update_layout(
        font_family="Georgia",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font=dict(size=20, family='Georgia', color='black')
    )
    charts.append(fig_scatter_matrix)

    return charts

# Load a subset of the dataset to avoid memory issues
file_path = 'D:/Downloads/final-year-project/data/final_subset_train_data.csv'
df = load_dataset(file_path)  # Load data
if df.empty:
    st.error("The dataset is empty or could not be loaded.")
else:
    df = preprocess_data(df)
# Define filters
filters = {}
excluded_columns = ["Unnamed: 0", "building_id"]

for column in df.columns:
    if column in excluded_columns:
        continue  # Skip the excluded columns
    if column == 'timestamp':
        start_date = df[column].min().date()
        end_date = df[column].max().date()
        filters[column] = st.sidebar.date_input(f"Select {column} range", [start_date, end_date], min_value=start_date, max_value=end_date)
    elif df[column].dtype == 'object' or df[column].nunique() < 20:
        unique_values = df[column].dropna().unique()  # Exclude NaN values from options
        filters[column] = st.sidebar.multiselect(f"Select {column}", options=unique_values, default=unique_values)
    else:
        min_val, max_val = df[column].min(), df[column].max()
        filters[column] = st.sidebar.slider(f"Select {column} range", min_value=float(min_val), max_value=float(max_val), value=(float(min_val), float(max_val)))

# Option to exclude NaN values
exclude_nan = st.sidebar.checkbox("Exclude NaN values", value=True)

# Apply filters
filtered_df = df.copy()
for column, filter_val in filters.items():
    if column == 'timestamp':
        start_date, end_date = filter_val
        filtered_df = filtered_df[(filtered_df[column].dt.date >= start_date) & (filtered_df[column].dt.date <= end_date)]
    elif isinstance(filter_val, list):
        filtered_df = filtered_df[filtered_df[column].isin(filter_val)]
    else:
        filtered_df = filtered_df[(filtered_df[column] >= filter_val[0]) & (filtered_df[column] <= filter_val[1])]

# Exclude NaN values if checkbox is selected
if exclude_nan:
    filtered_df = filtered_df.dropna()

# Building ID Filter with "Select All" option
building_ids = df['building_id'].unique().tolist()
building_ids.sort()
select_all = st.sidebar.checkbox("Select All building_id", value=False)

if select_all:
    selected_building_ids = building_ids
else:
    selected_building_ids = st.sidebar.multiselect(
        "Select building_id",
        options=building_ids,
        default=building_ids[:10] if building_ids else [],
        key="building_id_multiselect",
        help="Use the checkbox above to select/deselect all"
    )

# Apply building ID filter
if selected_building_ids:
    filtered_df = filtered_df[filtered_df['building_id'].isin(selected_building_ids)]

    # Calculate percentages
    total_buildings = filtered_df['building_id'].nunique()
    high_consumption_buildings = filtered_df[filtered_df['z_score'] > 2]['building_id'].nunique()
    low_consumption_buildings = total_buildings - high_consumption_buildings

    if total_buildings == 0:
        st.error("No data available for the selected filters.")
    else:
        high_consumption_percentage = (high_consumption_buildings / total_buildings) * 100
        low_consumption_percentage = (low_consumption_buildings / total_buildings) * 100

        # Display progress bars
        st.markdown("<h1 class='custom-title'>Building Energy Demand Dashboard</h1>", unsafe_allow_html=True)
  

        col1, col2 = st.columns([1, 3])

        with col1:
            st.plotly_chart(create_donut_chart(high_consumption_percentage, low_consumption_percentage))

        with col2:
            col21, col22, col23, col24 = st.columns(4)
            with col21:
                st.plotly_chart(create_indicator_chart(filtered_df['square_feet'].mean(), "Mean Square Feet"))
            with col22:
                st.plotly_chart(create_indicator_chart(filtered_df['meter_reading'].mean(), "Mean Meter Reading"))
            with col23:
                st.plotly_chart(create_indicator_chart(filtered_df['air_temperature'].mean(), "Mean Air Temperature"))
            with col24:
                st.plotly_chart(create_indicator_chart(filtered_df['wind_speed'].mean(), "Mean Wind Speed"))

        # Create and display the story_one
        story_one = create_story_one(filtered_df)

        # Save the story_one as HTML
        with open("story_one.html", "w") as f:
            f.write(story_one.to_html())

        # Display the generated HTML file
        with open("story_one.html", "r") as f:
            story_one_html = f.read()

        st.components.v1.html(story_one_html, height=650)

        # Display additional charts
        charts = create_additional_charts(filtered_df)
        for chart in charts:
            st.plotly_chart(chart, use_container_width=True)

# File Upload for Data Visualization
st.markdown("<h2 class='custom-title'>Upload Data for Visualization</h2>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, dtype=d_types)
        st.write("Uploaded Data")
        st.write(df)
        df = preprocess_data(df)
        filtered_df = df.copy()
        story_one = create_story_one(filtered_df)
        with open("story_one.html", "w") as f:
            f.write(story_one.to_html())
        with open("story_one.html", "r") as f:
            story_one_html = f.read()
        st.components.v1.html(story_one_html, height=650)
        charts = create_additional_charts(filtered_df)
        for chart in charts:
            st.plotly_chart(chart, use_container_width=True)
    except Exception as e:
        st.error(f"Error uploading file: {e}")

# Button to reset filters
if st.button('Reset Filters'):
    filtered_df = df.copy()
    story_one = create_story_one(filtered_df)
    with open("story_one.html", "w") as f:
        f.write(story_one.to_html())
    with open("story_one.html", "r") as f:
        story_one_html = f.read()
    st.components.v1.html(story_one_html, height=650)
    charts = create_additional_charts(filtered_df)
    for chart in charts:
        st.plotly_chart(chart, use_container_width=True)
